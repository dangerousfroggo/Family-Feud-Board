import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    questions = connection.execute('SELECT * FROM questions').fetchall()
    connection.close()
    return render_template('index.html', questions=questions)