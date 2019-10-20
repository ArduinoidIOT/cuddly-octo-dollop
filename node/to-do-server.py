from flask import Flask
import json

app = Flask(__name__)

data = []

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
    app.run(port=3000)
