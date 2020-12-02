from flask import Flask, render_template, request
import requests
import json

# App config
app = Flask(__name__)


@app.route("/", methods=['GET'])
def start():
    return render_template('index.html')


@app.route("/test", methods=['GET'])
def test():
    return render_template('test.html')


@app.route("/code", methods=['GET'])
def code():
    with open('main.py', 'r') as f:
        data = f.read().replace('<', '&lt;').replace('>', '&gt;')
    return render_template('code.html', data=data)


@app.route("/suggest", methods=['GET'])
def suggest():
    query = request.args.get('q')
    token = request.args.get('t')
    endpoint = request.args.get('e')
    username = request.args.get('u')
    password = request.args.get('p')
    url = endpoint + "?q=" + query

    if token != "":
        headers = {"Authorization": "Bearer " + token}
        r = requests.get(url, headers=headers)
    else:
        r = requests.get(url, auth=(username, password))

    rJson = json.loads(r.text)
    rList = []

    # use this when parsing Solr SUGGEST queries
    for x in rJson["suggest"]["Suggestions"][query]["suggestions"]:
        rList.append(x["term"])

    # use this when parsing Solr SELECT queries
    # for x in rJson["response"]["docs"]:
    #    rList.append(x["query"]) # 'query' should match the field name returned in the JSON docs list

    return str(rList).replace("\'", "\"")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)