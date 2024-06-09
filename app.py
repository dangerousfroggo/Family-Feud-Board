import os
from os import path
import json
from flask import Flask, render_template, request, redirect

from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)


#List for correct answers
answerlist = 'answers.json'
correct_answers = []

if path.isfile(answerlist) is False:
    raise exception("File not found")

#Google Sheets API
SERVICE_ACCOUNT_FILE = 'service-account.json'


SPREADSHEET_ID = '1k0SQWeCJDjrbasrXv8ZGvV9MMvW5aWWMsWxRjacvbyA'


RANGE_NAME = 'Sheet1!A1:Z1000'


credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
)
service = build('sheets', 'v4', credentials=credentials)


sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

def transpose_data(data):
    num_rows = len(data)
    num_columns = max(len(row) for row in data)
    
   
    transposed_data = []
    for col_idx in range(num_columns):
        column = []
        for row_idx in range(num_rows):
          
            if col_idx < len(data[row_idx]):
                column.append(data[row_idx][col_idx])
            else:
                column.append(None)
        transposed_data.append(column)
    
    return transposed_data

if not values:
    print('No data found.')
else:
    #The first row contains the questions
    questions = values[0]
    print(questions)
    #The following rows contain the answers
    
    answers = transpose_data(values[1:])
    print(answers)

class GetQuestionAnswers:
    def __init__(self, questions, answers, index=0):
        self.questions = questions
        self.answers = answers
        self.index = index
    
    def next_pair(self):
        if self.index >= len(self.answers):
            return None
        current_pair = (self.questions[self.index], self.answers[self.index])
        self.index += 1
        return current_pair

    def same_pair(self):
        return self.questions[self.index - 1], self.answers[self.index - 1]

reader = GetQuestionAnswers(questions, answers)



@app.route('/', methods=['GET', 'POST'])
def index():

    with open(answerlist) as fp:
        correct_answers = json.load(fp)

    question, answers = reader.same_pair()  
    
    if question:
        if request.method == 'POST':
            submitted_answer = request.form['submittedAnswer']
            if submitted_answer in answers:
                correct_answers.append(submitted_answer)
                with open(answerlist, 'w') as json_file:
                    json.dump(correct_answers, json_file)
        return render_template('index.html', question=question, answers=correct_answers)
    else:
        return "No more questions."

"""
@app.route('/answerpage', methods=['GET', 'POST'])
def answerpage():
    correct_answers = []
    question, answers = reader.same_pair()
    if question:
        if request.method == 'POST':
            submitted_answer = request.form['submittedAnswer']
            if submitted_answer in answers:
                correct_answers.append(submitted_answer)
        return render_template('answerpage.html', question=question[1], answers=answers[1:], correct_answers=correct_answers)
    else:
        return "No more questions."
"""

@app.route('/nextquestion/')
def next_question():
    pair = reader.next_pair()
    with open(answerlist, 'w') as json_file:
        json.dump([], json_file)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
