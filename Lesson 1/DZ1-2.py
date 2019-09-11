""""
Задание 2
Изучить список открытых API. Найти среди них любое,
которое требует авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию.
Результат ответа от сервера записать в файл.
"""
import requests
AccesToken = 'c653c7c9f7738a65997a7ae37907635cbb1014dc'
headers = {'Authorization': 'token ' + AccesToken}

r = requests.get('https://api.github.com/user', headers=headers)
r.json()
file = open('out2.json', 'w')
file.write(str(r.json()))
file.close()
r.close()