import socketserver
import sqlite3
import pickle
import time

# c.execute("INSERT INTO messages(content, userId, roomId) VALUES ()")

conn = sqlite3.connect('chat.db')
c = conn.cursor()

class MyTCPHandler(socketserver.BaseRequestHandler):

    def checkLoggedIn(self, u,p):
        c.execute("SELECT rowid FROM users WHERE username=? AND password=?", (u,p))
        rows = c.fetchall()
        if len(rows) > 0:
            print("user and password found")
            return True
        else:
            print("user and password not found")
            return False

    def checkRoomExists(self, n):
        c.execute("SELECT rowid FROM rooms WHERE name=?", (n,))
        rows = c.fetchall()
        for row in rows:
            return row[0]
        return False

    def checkRoomPublic(self, n):
        private = -1
        c.execute("SELECT private FROM rooms WHERE name=?", (n,))
        rows = c.fetchall()
        for row in rows:
            private = row[0]
        if private == 0:
            return True
        else:
            return False

    def joinRoom(self, n,p=""):
        if not self.checkRoomPublic(n):
            c.execute("SELECT rowid FROM rooms WHERE name=? and password=?", (n,p))
            rows = c.fetchall()
            for row in rows:
                return row[0]
            return False
        else:
            return self.checkRoomExists(n)

    def sendMessage(self, u,n,m):
        print("sending message...")
        try:
            c.execute("SELECT rowid FROM users WHERE username=?", (u,))
            rows = c.fetchall()
            for row in rows:
                u=row[0]
            c.execute("SELECT rowid FROM rooms WHERE name=?", (n,))
            rows = c.fetchall()
            for row in rows:
                n=row[0]
            c.execute("INSERT INTO messages(userId,roomId,content, timePosted) VALUES (?,?,?,?) ",(u,n,m,time.time()))
            conn.commit()
            return True
        except:
            return False

    def getMessages(self, n,p):
        arr = []
        if self.joinRoom(n,p):
            c.execute("SELECT userId, content FROM messages WHERE roomId=? ORDER BY timePosted ASC LIMIT 10",(self.checkRoomExists(n),))
            rows = c.fetchall()
            for row in rows:
                c.execute("SELECT username FROM users WHERE rowid=?",(row[0],))
                rowws = c.fetchall()
                for roww in rowws:
                    arr.append(roww[0] + ": " + row[1])
        return arr

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = pickle.loads(self.request.recv(1024))
        # print("{} sent:".format(self.client_address[0]))
        # print(self.data)

        # log in
        if self.data[0] == 1:
        # take:
        # [ID, uName, pWord]
        # return:
        # [loginSuccess?]
            loginSuccess = self.checkLoggedIn(self.data[1],self.data[2])
            self.request.sendall(pickle.dumps([loginSuccess]))

        # send a message
        elif self.data[0] == 2:
        # take:
        # [ID, uName, pWord, room, password, content]
        # return:
        # [loginSuccess?, roomSuccess?, messageSuccess?]


            messageSuccess = False

            loginSuccess = self.checkLoggedIn(self.data[1],self.data[2])

            roomSuccess = self.joinRoom(self.data[3],self.data[4])

            if loginSuccess and roomSuccess:
                messageSuccess = self.sendMessage(self.data[1],self.data[3],self.data[5])
                if messageSuccess:
                    # do more stuff here
                    print("{} says:".format(self.client_address[0]))
                    print(self.data[3])
            print([loginSuccess, roomSuccess, messageSuccess])
            self.request.sendall(pickle.dumps([loginSuccess, roomSuccess, messageSuccess]))

        # join a room or say that it has a password
        elif self.data[0] == 3:
        # take:
        # [ID, uName, pWord, room]
        # return:
        # [loginSuccess?, roomSuccess?]

        # roomSuccess:
        # 0 - does not exist
        # 1 - exists, no password
        # 2 - exists, has password
            msgs = []
            roomSuccess = 0

            loginSuccess = self.checkLoggedIn(self.data[1],self.data[2])

            if self.checkRoomExists(self.data[3]):
                if self.checkRoomPublic(self.data[3]):
                    roomSuccess = 1
                    msgs = self.getMessages(self.data[3],"")
                else:
                    roomSuccess = 2

            self.request.sendall(pickle.dumps([loginSuccess, roomSuccess, msgs]))
        # join a room if it has a password (not done)
        elif self.data[0] == 4:
        # take:
        # [ID, uName, pWord, room, password]
        # return:
        # [loginSuccess?, roomSuccess?]

        # roomSuccess:
        # 0 - does not exist
        # 1 - exists, no password
        # 2 - exists, has password
            msgs = []
            roomSuccess = 0

            loginSuccess = self.checkLoggedIn(self.data[1],self.data[2])

            if self.checkRoomExists(self.data[3]):
                if self.checkRoomPublic(self.data[3]):
                    roomSuccess = 1
                    msgs = self.getMessages(self.data[3],"")
                else:
                    roomSuccess = 2

            self.request.sendall(pickle.dumps([loginSuccess, roomSuccess, msgs]))



if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
