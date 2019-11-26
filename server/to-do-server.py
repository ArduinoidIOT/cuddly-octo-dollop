#!/usr/bin/python
from flask import Flask, redirect, request
import json

app = Flask(__name__)

database = {}


@app.route('/')
def goto():
    return redirect('static/to-do.html', 301)


@app.route('/todolists/', methods=['GET', 'POST', 'DELETE'])
def hello_world():
    data = request.data.decode()
    if request.method == 'POST':
        if data not in database.keys() and len(data) < 12 and data != '':
            database[data] = []
    if request.method == 'DELETE':
        if data in database.keys() and len(database.keys()) > 1:
            del database[data]
    return json.dumps(list(database.keys()))


@app.route('/todolists/<name>/tasks', methods=['GET', 'POST'])
def gettodotilts(name):
    data = request.data.decode()
    if request.method == 'POST':
        data = json.loads(data)
        if data['text'] != '':
            database[name].append(data)
    return json.dumps(database[name])


@app.route('/todolists/<name>/cct', methods=['POST'])
def cct(name):
    data = []
    for i in database[name]:
        if not i['checked']:
            data.append(i)
    database[name] = data
    return json.dumps(database[name])


@app.route('/todolists/<name>/tasks/count/')
def gettaskcount(name):
    nonchecked = 0
    for i in database[name]:
        if not i['checked']:
            nonchecked += 1
    return json.dumps({'total': len(database[name]), 'todo': nonchecked})


@app.route('/todolists/<name>/<id>/toggleChecked/', methods=['POST'])
def toggleChecked(name, id):
    stat = 200
    try:
        id = int(id)
        database[name][id]['checked'] = not database[name][id]['checked']
    except ValueError:
        stat = 400
    nonchecked = 0
    for i in database[name]:
        if not i['checked']:
            nonchecked += 1
    return json.dumps({'total': len(database[name]), 'todo': nonchecked}), stat


if __name__ == '__main__':
    app.run(port=3000)
