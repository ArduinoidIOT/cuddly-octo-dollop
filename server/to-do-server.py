#!/usr/bin/python3
from flask import Flask, request, make_response, redirect
from os import urandom
from binascii import hexlify
import json
from hashlib import sha256

app = Flask(__name__)

database = {"rohan": {'YouTube': []}, "mohan": {'YouTube': []}}
sessions = {}
userBase = {'rohan': '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
            'mohan': "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"}


def getUser(sid):
    return sessions.get(sid)


@app.route('/todolists/', methods=['GET', 'POST', 'DELETE'])
def hello_world():
    data = request.data.decode()
    user = getUser(request.cookies.get('sessionid'))
    if not user:
        return '', 401
    if request.method == 'POST':
        if data not in database[user].keys() and len(data) < 12:
            database[user][data] = []
    if request.method == 'DELETE':
        if data in database[user].keys() and len(database[user].keys()) > 1:
            del database[user][data]
    return json.dumps(list(database[user].keys()))


@app.route('/todolists/<name>/tasks', methods=['GET', 'POST'])
def gettodotilts(name):
    user = getUser(request.cookies.get('sessionid'))
    if not user:
        return '', 401
    data = request.data.decode()
    if request.method == 'POST':
        data = json.loads(data)
        if data['text'] != '':
            database[user][name].append(data)
    return json.dumps(database[user][name])


@app.route('/todolists/<name>/cct', methods=['POST'])
def cct(name):
    data = []
    user = getUser(request.cookies.get('sessionid'))
    if not user:
        return '', 401
    for i in database[user][name]:
        if not i['checked']:
            data.append(i)
    database[user][name] = data
    return json.dumps(database[user][name])


@app.route('/todolists/<name>/tasks/count/')
def gettaskcount(name):
    nonchecked = 0
    user = getUser(request.cookies.get('sessionid'))
    if not user:
        return '', 401
    for i in database[user][name]:
        if not i['checked']:
            nonchecked += 1
    return json.dumps({'total': len(database[user][name]), 'todo': nonchecked})


@app.route('/todolists/<name>/<id>/toggleChecked/', methods=['POST'])
def toggleChecked(name, id):
    stat = 200
    user = getUser(request.cookies.get('sessionid'))
    if not user:
        return '', 401
    try:
        id = int(id)
        database[user][name][id]['checked'] = not database[user][name][id]['checked']
    except ValueError:
        stat = 400
    nonchecked = 0
    for i in database[user][name]:
        if not i['checked']:
            nonchecked += 1
    return json.dumps({'total': len(database[user][name]), 'todo': nonchecked}), stat


@app.route('/login', methods=['POST'])
def authenticate():
    data = request.data
    data2 = {}
    if data == b'':
        data = request.form
    else:
        data = json.loads(data)
    print(data)
    data2['user'] = data['user'].strip()
    data2['password'] = data['password'].strip()
    if data2['user'] not in userBase.keys():
        return '', 403
    hash = sha256()
    hash.update(data2['password'].encode())
    print(hash.hexdigest(), data2['password'].encode())
    if userBase[data2['user']] != hash.hexdigest():
        return '', 403
    session_cookie = hexlify(urandom(18)).decode()
    sessions[session_cookie] = data2['user']
    response = make_response(redirect('/'))
    response.set_cookie('sessionid', session_cookie)
    print(sessions)
    return response


@app.route('/logged_in')
def hello():
    name = request.cookies.get('sessionid')
    print(name)
    if name not in sessions.keys():
        return '', 403
    return '<h1>' + sessions[
        name] + '</h1><form action=\'/logout\' method=\'POST\'><button type="submit">Logout </button></form>'


@app.route('/logout', methods=['POST'])
def logout():
    user = getUser(request.cookies.get('sessionid'))
    if not user:
        return '', 401
    del sessions[user]
    resp = make_response(redirect('/'))
    resp.set_cookie('sessionid', '')
    return resp


@app.route('/static/to-do.html')
def handleNoAuth():
    name = request.cookies.get('sessionid')
    if getUser(name):
        with open('static/to-do.html') as todohtml:
            return todohtml.read()
    else:
        return redirect('/static/Login.html')


@app.route('/')
def goto():
    return redirect('/static/to-do.html')
    name = request.cookies.get('sessionid')
    if name and getUser(name):
        return redirect('/static/to-do.html')
    else:
        return redirect('/static/Login.html')


@app.route('/static/Login.html')
def handleAuthenticated():
    name = request.cookies.get('sessionid')
    if not getUser(name):
        with open('static/Login.html') as loginhtml:
            return loginhtml.read()
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
