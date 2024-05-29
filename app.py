import ast
from flask import Flask, render_template
import json

app = Flask(__name__)
filepath = 'questions.json'

class GetQuestionAnswers:
    def __init__(self, filepath, index=0):
        self.filepath = filepath
        self.pairs = self.load_pairs()
        self.index = index
    
    def load_pairs(self):
        with open(self.filepath, 'r') as file:
            content = file.read()
            return json.loads(content)
    
    def next_pair(self):
        if self.index >= len(self.pairs):
            return None
        current_pair = list(self.pairs.items())[self.index]
        self.index += 1
        return current_pair

reader = GetQuestionAnswers(filepath)

@app.route('/')
def index():
    pair = reader.next_pair()
    if pair:
        question, answers = pair
        return render_template('index.html', question=question, answers=answers)
    else:
        return "No more questions."

if __name__ == '__name__':
    app.run(debug=True)