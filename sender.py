import requests
import time
from datetime import datetime
import threading

# domen = "http://5.53.124.89"
domen = "http://localhost"
port_id = ':5000'
response = requests.get(domen + port_id + "/status")
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

while True:
    try:
        time.sleep(0.5)
        print("Введите сообщение:")
        text = input()
        response = requests.post(
            domen + port_id + "/send",
            json={"username": username, "password": password, "text": text}
        )
            print()
        except ConnectionError:
            print("Попытка соединения не удалась")
            print()
