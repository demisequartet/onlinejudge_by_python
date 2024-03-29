from flask import Flask, request, jsonify, render_template
from judge import main
import dbaccess
from waitress import serve

import urllib.parse
app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/top', methods=['GET', 'POST'])
def top():
    return render_template('top.html')


@app.route('/question/<int:questionID>', methods=['GET', 'POST'])
def question(questionID):
    questionInfo = dbaccess.getQuestion(questionID)
    return render_template('index.html', question=questionInfo) if questionInfo else f'<h1>Question {questionID} not found</h1>'


@app.route('/choice', methods=['POST', 'GET'])
def choice():
    return render_template('choice.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    submits = dbaccess.getALLsubmit()
    print("result")
    print(submits)

    return render_template('result.html', submits=submits)


@app.route('/getALLsubmits', methods=['POST', 'GET'])
def getALLsubmits():
    contents = jsonify(dbaccess.getALLsubmit())

    return contents


@ app.route('/submit_sourcecode', methods=['POST'])
def judge():
    print("judge")
    questionID = int(request.form['questionID'])
    encodedSource = request.form['source']
    studentID = request.form['studentID']
    source = urllib.parse.unquote(encodedSource)

    print("questionID: ", questionID)
    print("source: ", source)
    print("studentID: ", studentID)

    dbaccess.outputTofile(questionID)

    result = main(source)
    # encodedResult = urllib.parse.quote(result)

    # print(result)
    # source = source.replace('\n', '<br>')
    resID = dbaccess.registerSource(studentID, questionID,
                                    result, source)

    # resID = dbaccess.getResponseID(studentID, questionID, result, source)

    return jsonify({"result": result, "responseID": resID})


@ app.route('/getALLQuestions', methods=['GET', 'POST'])
def getALLQuestions():
    return jsonify(dbaccess.getALLQuestions())


# https://qiita.com/ekzemplaro/items/2766618ba5968ee62b70
# host='0.0.0.0' でないとdockerで動かした際に、host側で見ることができない
# threaded = true 同時アクセス制御
development = True

if development:
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
else:
    serve(app, host='0.0.0.0', port=8000)
