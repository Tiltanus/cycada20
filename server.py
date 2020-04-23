#!/usr/bin/env python3
import time
from datetime import datetime
import codecs
from flask import Flask, request

app = Flask(__name__)
port_id = 5000
level = 0
sended = False
level_change = False
users = {'root': '2'}
messages = []
file = open("login.txt", "r")
for line in file:
    key, *value = line.split()
    users[key] = value
file.close()


def bad_answer():
    global sended
    sended = True
    messages.clear()
    messages.append({"username": "SYSTEM", 'text': 'Ответ неверный', 'time': time.time()})


def good_answer():
    global sended
    sended = True
    global level
    level += 1
    global level_change
    level_change = True
    messages.clear()
    messages.append({"username": "SYSTEM", 'text': 'Ответ принят', 'time': time.time()})


def messages_for_current_task():
    task = []
    file = codecs.open("./levels/" + str(level) + "/" + str(level) + "_task.txt", "r", "utf-8")
    for line in file.readlines():
        task.append({'username': 'SYSTEM', 'text': line, 'time': time.time()})
    return task


def hint_for_current_task():
    global sended
    sended = True
    messages.clear()
    file = codecs.open("./levels/" + str(level) + "/" + str(level) + "_hint.txt", "r", "utf-8")
    for line in file.readlines():
        messages.append({'username': 'SYSTEM', 'text': line, 'time': time.time()})


def answer_for_current_task():
    answer = []
    file = codecs.open("./levels/" + str(level) + "/" + str(level) + "_answer.txt", "r", "utf-8")
    for line in file.readlines():
        answer.append(line)
    return answer


@app.route("/")
def hello_view():
    return {'answer': sended}


@app.route("/status")
def status_view():
    return {
        'status': True,
        'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'level': level
    }


@app.route("/task")
def task_0():
    global sended
    sended = False
    global level_change
    level_change = False
    return {'messages': messages_for_current_task()}


@app.route("/messages")
def messages_view():
    global sended
    sended = False
    return {'messages': messages, 'level++': level_change}


@app.route("/send", methods=['POST'])
def send_view():
    """
    Отправка сообщений
    input: {
        "username": str,
        "password": str,
        "text": str
    }
    output: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users or users[username] != password:
        return {"ok": False}
    if data["text"] == 'hint':
        hint_for_current_task()
    else:
        text = data["text"]
        if text in answer_for_current_task():
            good_answer()
        else:
            bad_answer()
        return {'ok': True}


@app.route("/auth", methods=['POST'])
def auth_view():
    """
    Авторизовать пользователя или сообщить что пароль неверный.
    input: {
        "username": str,
        "password": str
    }
    output: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users:
        return {"ok": False}
    elif users[username] == password:
        return {"ok": True}
    else:
        return {"ok": False}


app.run(host='0.0.0.0', port=port_id)
# TODO: добавить уровни
