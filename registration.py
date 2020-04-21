import time
from datetime import datetime
from threading import Thread
import requests

domen = "http://3.21.168.161"
# domen = "http://localhost"
port_id = "5000"
last_time = 0


def auth_request(username, password):
    response = requests.post(
        domen + ':' + port_id + "/auth",
        json={"username": username, "password": password}
    )
    return response


# variable = Thread(target=auth_request())

response = requests.get(domen + ':' + port_id + "/status")
status = response.json()['status']
if status:
    print(response.text)
else:
    print("Удалённый сервер недоступен, вы будете отключены через 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    exit(0)

print("Введите имя:")
username = input()

print("Введите пароль:")
password = input()

print("Дождитесь ответа от сервера!")
response = auth_request(username, password)

if not response.json()['ok']:
    print('Имя занято, попробуйте ещё раз')
while not response.json()['ok']:
    print("Введите имя:")
    username = input()

    print("Введите пароль:")
    password = input()
    print("Дождитесь ответа от сервера!")
    response = auth_request(username, password)
    if not response.json()['ok']:
        print('Имя занято')

response = requests.get(domen + ':' + port_id + "/messages",
                        params={'after': last_time, 'username': username})
messages = response.json()["messages"]

for message in messages:
    beauty_time = datetime.fromtimestamp(message["time"])
    beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
    print(message["username"], beauty_time)
    print(message["text"])
    print()

    last_time = message["time"]
print("Нажмите любую клавишу, чтобы закрыть окно")
input()
exit()
# TODO: распараллелить аутентификацию
