import sqlite3
import bcrypt

# connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')

# create a cursor object to execute SQL commands
c = conn.cursor()

# create a table to store user credentials
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              password TEXT)''')

# get the user's input (e.g. from a form)
#username = 'admin'
#password = 'admin'

# hash the password using bcrypt
#hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# insert the user into the database
#c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))

c.execute('SELECT * FROM users')
result = c.fetchall()
print(result)

# commit the changes and close the connection
conn.commit()
conn.close()
