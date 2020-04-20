#!/usr/bin/env python
import time
from datetime import datetime

from flask import Flask, request

app = Flask(__name__)
messages = [
    {"username": "Jack", "text": "Hello!", "time": time.time()},
    {"username": "Mary", "text": "Hi, Jack", "time": time.time()},
]
users = {
    'Jack': '12345',
    'Mary': '54321',
}


@app.route("/")
def hello_view():
    return "<h1>Welcome to Python messenger!</h1>"


@app.route("/status")
def status_view():
    return {
        'status': True,
        'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }


@app.route("/users")
def users_view():
    return {'users': users}


@app.route("/last_message")
def last_message_view():
    return {'messages': messages}


@app.route("/messages")
def messages_view():
    """
    Получение сообщений после отметки after
    input: after - отметка времени
    output: {
        "messages": [
            {"username": str, "text": str, "time": float},
            ...
        ]
    }
    """
    after = float(request.args['after'])
    username = request.args['username']
    if username =="admin":
        new_messages = [message for message in messages if message['time'] > after]
    else:
        new_messages = [message for message in messages if message['time'] > after and (message['username'] == username or message['username'] == 'admin')]
    return {'messages': new_messages}


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

    text = data["text"]
    messages.append({"username": username, "text": text, "time": time.time()})

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
        users[username] = password
        return {"ok": True}
    elif users[username] == password:
        return {"ok": True}
    else:
        return {"ok": False}


app.run(host='0.0.0.0', port=5000)
# TODO: сервер возвращает только сообщения админа и пользователя
