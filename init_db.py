import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO questions (question, answers) VALUES (?, ?)", ('Members of the tiktok rizz party', 'blue tie kid, turkish quandale dingle'))

connection.commit()
connection.close()