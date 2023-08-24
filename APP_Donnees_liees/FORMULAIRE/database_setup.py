import sqlite3

# Open a connection to the database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Execute a SELECT query to fetch all rows from the `parcs` table
c.execute("SELECT * FROM parcs")
rows = c.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()
