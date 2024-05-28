import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO questions (question, answers) VALUES (?, ?)", ('sample question', 'sample answer'))

connection.commit()
connection.close()