import requests
import json

i = 1
# имя пользователя GitHub
username = 'RiK-pro'
result = requests.get(f'https://api.github.com/users/{username}/repos')
data = result.json()
filename = f'{username}.json'

print(f'Список открытых репозиториев пользователя {username}')

for el in data:
    print(i, el['name'])
    i += 1

print(f'Записываем исходные данные в файл {username}.json')

with open(filename, "w") as write_f:
    json.dump(data, write_f, indent=1)