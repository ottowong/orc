import socket
import sys
import pickle
import getpass

HOST, PORT = "localhost", 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create a socket (SOCK_STREAM means a TCP socket)

def inRoom(uName, pWord, room, roomPw):
    while True:
        try:
            message = input(uName + ": ")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            sock.sendall(pickle.dumps([2, uName, pWord, room, roomPw, message]))
            received = pickle.loads(sock.recv(1024))
            if received[0] and received[1] and received[2]:
                pass
            else:
                print("Failed to send message :(")
        finally:
            sock.close()

def loggedIn(uName, pWord):
    while True:
        try:
            print("Enter a room name to join (e.g. 'main')")
            roomName = input("r: ")
            roomPw = ""
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            sock.sendall(pickle.dumps([3, uName, pWord, roomName]))
            received = pickle.loads(sock.recv(1024))
            if received[0]:
                if received[1] == 1:
                    print("..........")
                    print("Joined room '" + roomName + "'")
                    print("..........")
                    for thing in received[2]:
                        print(thing)
                    print("..........")
                    inRoom(uName,pWord,roomName,roomPw)
                else:
                    sock.close()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((HOST, PORT))
                    print("Enter password for room '" + roomName + "'")
                    roomPw = input("p: ")
                    sock.sendall(pickle.dumps([4, uName, pWord, roomName, roomPw]))
            else:
                print("Could not join room!")
                return
        finally:
            sock.close()

while True:
    try:
        print("Log in")
        uName = input("u: ")
        pWord = getpass.getpass("p: ")
        # Connect to server and send data
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(pickle.dumps([1,uName,pWord]))
        # sock.sendall(bytes(data + "\n", "utf-8"))

        # Receive data from the server and shut down
        received = pickle.loads(sock.recv(1024))
        if received[0]:
            print("Success!")
            loggedIn(uName, pWord)
        else:
            print("Incorrect login!")

    finally:
        sock.close()

print("Received: {}".format(received))
