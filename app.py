from flask import Flask, request, jsonify, render_template
from judge import main
import dbaccess

import urllib.parse
app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/<int:questionID>', methods=['GET', 'POST'])
def index(questionID):
    questionInfo = dbaccess.getQuestion(questionID)
    return render_template('index.html', question=questionInfo)


@app.route('/choice', methods=['POST', 'GET'])
def choice():
    return render_template('choice.html')


@app.route('/submit_sourcecode', methods=['GET', 'POST'])
def judge():
    print("judge")
    source = request.args.get('source')
    source = urllib.parse.unquote(source)
    print(source)

    result = main(source)

    print(result)

    return jsonify({"result": result})


@app.route('/getALLQuestions', methods=['GET', 'POST'])
def getALLQuestions():
    return jsonify(dbaccess.getALLQuestions())


app.run(port=8000, debug=True)
