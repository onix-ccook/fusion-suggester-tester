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
    elif username != "" and password != "":
        r = requests.get(url, auth=(username, password))
    else:
        r = requests.get(url)

    if r.status_code != 200:
        err = str(r.status_code) + " error on backend request"
        return str([err]).replace("\'", "\"")

    r_json = json.loads(r.text)
    r_list = []

    # use this when parsing Solr SUGGEST queries
    for x in r_json["suggest"]["Suggestions"][query]["suggestions"]:
        r_list.append(x["term"])

    # use this when parsing Solr SELECT queries
    # for x in r_json["response"]["docs"]:
    #    r_list.append(x["query"]) # 'query' should match the field name returned in the JSON docs list

    return str(r_list).replace("\'", "\"")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
