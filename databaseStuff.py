import sqlite3
conn = sqlite3.connect('chat.db')

c = conn.cursor()

# c.execute("CREATE TABLE users(username text, email text, password text)")
# c.execute("INSERT INTO users (username, email, password) VALUES ('otto','otto@email.com','password')")
#
# c.execute("CREATE TABLE rooms(name text, private integer, password text, userId integer, foreign key(userId) references users(rowid))")
# c.execute("INSERT INTO rooms (name, private, userId) VALUES ('main','0','1')")
#
# c.execute("CREATE TABLE messages(content text, userId integer, roomId integer, timePosted integer, foreign key(userId) references users(rowid), foreign key(roomId) references rooms(rowid))")

# c.execute("DELETE FROM messages")

# c.execute("SELECT rowid, * FROM rooms")
# rows = c.fetchall()
# for row in rows:
#     print(row)

# c.execute("SELECT rowid, * FROM messages")
# rows = c.fetchall()
# for row in rows:
#     print(row)

conn.commit()
conn.close()
