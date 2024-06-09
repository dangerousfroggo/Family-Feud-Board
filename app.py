import os
from flask import Flask, render_template, request, redirect

from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)


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


if not values:
    print('No data found.')
else:
    #The first row contains the questions
    questions = values[0]
    
    #The following rows contain the answers
    answers = values[1:]

class GetQuestionAnswers:
    def __init__(self, questions, answers, index=0):
        self.questions = questions
        self.answers = answers
        self.index = index
    
    def next_pair(self):
        if self.index >= len(self.answers):
            return None
        current_pair = (self.questions, self.answers[self.index])
        self.index += 1
        return current_pair

    def same_pair(self):
        return self.questions, self.answers[self.index - 1]

reader = GetQuestionAnswers(questions, answers)

@app.route('/', methods=['GET', 'POST'])
def index():
    correct_answers = []
    question, answers = reader.same_pair()  
    
    if question:
        if request.method == 'POST':
            submitted_answer = request.form['submittedAnswer']
            if submitted_answer in answers:
                correct_answers.append(submitted_answer)
        return render_template('index.html', question=question[1], answers=answers[1:])
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
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

