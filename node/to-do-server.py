from flask import Flask,redirect
import json

app = Flask(__name__)

data = []
@app.route('/')
def goto():
    return redirect('static/to-do.html',301)
@app.route('/todolists')
def hello_world():
    return json.dumps(data)
    print(data)

@app.route('/todolists/delete/<name>',methods=['POST'])
def deleteTodo(name):
    if name not in data:
        pass
    else:
        data.remove(name)
    return ""

@app.route('/todolists/create/<name>',methods=['POST'])
def createTodo(name):
    if name not in data:
        data.append(name)
        print(data)
        return "Success"
    print(data)
    return "Fail"

if __name__ == '__main__':
    app.run(port=5000)
