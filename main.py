from flask import Flask, request, jsonify
from judge import main

import urllib.parse
app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/', methods=['GET', 'POST'])
def index():
    return app.send_static_file('user/index.html')


@app.route('/submit_sourcecode', methods=['GET', 'POST'])
def judge():
    print("judge")
    source = request.args.get('source')
    source = urllib.parse.unquote(source)
    print(source)

    result = main(source)

    print(result)

    return jsonify({"result": result})


app.run(port=8000, debug=True)
