#!/usr/bin/python3
from flask import Flask, redirect, request
import json

app = Flask(__name__)

database = {"defaultUser": {'YouTube':[]}}


@app.route('/')
def goto():
    return redirect('static/to-do.html', 301)


@app.route('/todolists/', methods=['GET', 'POST', 'DELETE'])
def hello_world():
    data = request.data.decode()
    if request.method == 'POST':
        if data not in database['defaultUser'].keys() and len(data) < 12:
            database['defaultUser'][data] = []
    if request.method == 'DELETE':
        if data in database['defaultUser'].keys():
            del database['defaultUser'][data]
    return json.dumps(list(database['defaultUser'].keys()))


@app.route('/todolists/<name>/tasks', methods=['GET', 'POST'])
def gettodotilts(name):
    data = request.data.decode()
    if request.method == 'POST':
        data = json.loads(data)
        if data['text'] != '':
            database['defaultUser'][name].append(data)
    return json.dumps(database['defaultUser'][name])


@app.route('/todolists/<name>/cct', methods=['POST'])
def cct(name):
    data = []
    for i in database['defaultUser'][name]:
        if not i['checked']:
            data.append(i)
    database['defaultUser'][name] = data
    return json.dumps(database['defaultUser'][name])


@app.route('/todolists/<name>/tasks/count/')
def gettaskcount(name):
    nonchecked = 0
    for i in database['defaultUser'][name]:
        if not i['checked']:
            nonchecked += 1
    return json.dumps({'total': len(database['defaultUser'][name]), 'todo': nonchecked})


@app.route('/todolists/<name>/<id>/toggleChecked/', methods=['POST'])
def toggleChecked(name, id):
    stat = 200
    try:
        id = int(id)
        database['defaultUser'][name][id]['checked'] = not database['defaultUser'][name][id]['checked']
    except ValueError:
        stat = 400
    nonchecked = 0
    for i in database['defaultUser'][name]:
        if not i['checked']:
            nonchecked += 1
    return json.dumps({'total': len(database['defaultUser'][name]), 'todo': nonchecked}),stat


if __name__ == '__main__':
    app.run(port=3000)
