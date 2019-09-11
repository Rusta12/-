"""""
Задание 1
Посмотреть документацию к API гитхаба, разобраться как вывести
список репозиториев для конкретного пользователя, сохранить JSON-вывод
в файле *.json
"""

import requests
from pprint import pprint

headers = {'User-agent':'Chrome/76.0.3809.132'}

link = 'https://api.github.com/search/users'
username = 'Rust12'

aditional_settings = 'simple=yes&per_page=1&page=1'

r = requests.get(f'{link}?q={username}&{aditional_settings}',headers = headers)
r.json()
pprint(r.text)
file = open('out.json', 'w')
file.write(str(r.json()))
r.close()

