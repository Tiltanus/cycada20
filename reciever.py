import time
from datetime import datetime

import requests

# domen = "http://5.53.124.89"
domen = "http://localhost"
last_time = 0
level = -1
port_id = ":5000"

try:
    response = requests.get(domen + port_id + "/status")
    status = response.json()['status']
    if status:
        level = response.json()['level']
except:
    print("Удалённый сервер недоступен, вы будете отключены через 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    exit(0)
print(response.text)

print("Введите имя:")
username = input()

print("Введите пароль:")
password = input()

response = requests.post(
    domen + port_id + "/auth",
    json={"username": username, "password": password}
)
if not response.json()['ok']:
    print('Неверный пароль')

while not response.json()['ok']:
    print("Введите имя:")
    username = input()

    print("Введите пароль:")
    password = input()

    response = requests.post(
        domen + port_id + "/auth",
        json={"username": username, "password": password}
    )
    if not response.json()['ok']:
        print('Неверный пароль')

response = requests.get(domen + port_id + "/task",
                        params={'after': last_time})
messages = response.json()["messages"]

for message in messages:
    beauty_time = datetime.fromtimestamp(message["time"])
    beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
    print(message["username"], beauty_time)
    print(message["text"])
    print()

    last_time = message["time"]

response = requests.get(domen + port_id)

while True:
    while not response.json()['answer']:
        response = requests.get(domen + port_id)
    response = requests.get(domen + port_id + "/messages",
                            params={'after': last_time})
    messages = response.json()["messages"]
    for message in messages:
        beauty_time = datetime.fromtimestamp(message["time"])
        beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
        print(message["username"], beauty_time)
        print(message["text"])
        print()

        last_time = message["time"]
    if response.json()['level++']:
        level += 1
        response = requests.get(domen + port_id + "/task",
                                params={'after': last_time})
        messages = response.json()["messages"]

        for message in messages:
            beauty_time = datetime.fromtimestamp(message["time"])
            beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
            print(message["username"], beauty_time)
            print(message["text"])
            print()

            last_time = message["time"]
    response = requests.get(domen + port_id)
