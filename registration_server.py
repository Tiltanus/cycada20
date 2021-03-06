#!/usr/bin/env python3
import time
from datetime import datetime

from flask import Flask, request, send_from_directory

app = Flask(__name__)
port_id = 5000
messages = [
    {"username": "SYSTEM", "text": "Вы были успешно зарегистрированы.", "time": time.time()},
    {"username": "SYSTEM", "text": "Ждите дальнейших указаний в группе ИИТиАД ИРНИТУ", "time": time.time()},
]

"""
    username:password
    'admin': 't6q79uct',
    'neadmin': '1',
    'root': '2'
"""
users = {}

file = open("login.txt", "r")
for line in file:
    key, *value = line.split()
    users[key] = value
file.close()


@app.route("/")
def hello_view():
    return {}


@app.route("/status")
def status_view():
    return {
        'status': True,
        'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }


@app.route("/users")
def users_view():
    return send_from_directory('/usr/cycada20/cycada20', 'login.txt')


@app.route("/vk")
def vk_view():
    return send_from_directory('/usr/cycada20/cycada20', 'vk.txt')

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
    new_messages = [message for message in messages if message['time'] > after]
    return {'messages': new_messages}


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
    vk = data["vk"]

    if username not in users:
        users[username] = password
        file = open("login.txt", 'a')
        file.write('\n' + username + ' ' + password)
        file.close()
        file = open("vk.txt", "a")
        file.write('\n' + username + ' ' + vk)
        file.close()
        return {"ok": True}
    else:
        return {"ok": False}


app.run(host='0.0.0.0', port=port_id)
