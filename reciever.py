import time
from datetime import datetime

import requests
domen = "http://5.53.124.89"
last_time = 0

response = requests.get(domen + ":5000/status")
print(response.text)

print("Введите имя:")
username = input()

print("Введите пароль:")
password = input()

response = requests.post(
    domen + ":5000/auth",
    json={"username": username, "password": password}
)
if not response.json()['ok']:
    print('Неверный пароль')
    exit()

while True:
    response = requests.get(domen + ":5000/messages",
                            params={'after': last_time, 'username': username})
    messages = response.json()["messages"]

    for message in messages:
        beauty_time = datetime.fromtimestamp(message["time"])
        beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
        print(message["username"], beauty_time)
        print(message["text"])
        print()

        last_time = message["time"]

    time.sleep(1)
