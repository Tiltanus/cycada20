import time
from datetime import datetime
from threading import Thread
import requests

domen = "http://18.222.169.160"
# domen = "http://localhost"
port_id = "5000"
last_time = 0


def auth_request(username, password, vk):
    response = requests.post(
        domen + ':' + port_id + "/auth",
        json={"username": username, "password": password, "vk": vk}
    )
    return response


# variable = Thread(target=auth_request())
try:
    response = requests.get(domen + ':' + port_id + "/status")
    status = response.json()['status']
    if status:
        print(response.text)
except:
    print("Удалённый сервер недоступен, вы будете отключены через 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    exit(0)

print("Project CHARON. Пожалуйста, зарегистрируйтесь.")
print("Все поля являются обязательными.")
print("Введите имя:")
username = input()

print("Введите пароль:")
password = input()

print("Ссылка на вашу страницу необходима для подтверждения вашей личности")
print("Введите ссылку на вашу страницу VK:")
vk = input()

print("Дождитесь ответа от сервера!")
response = auth_request(username, password, vk)

if not response.json()['ok']:
    print('Имя занято, попробуйте ещё раз')
while not response.json()['ok']:
    print("Введите имя:")
    username = input()

    print("Введите пароль:")
    password = input()

    print("Введите вашу ссылку VK:")
    vk = input()

    print("Дождитесь ответа от сервера!")
    response = auth_request(username, password, vk)
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
input("Нажмите Enter чтобы закрыть окно")
exit()
# TODO: распараллелить аутентификацию
