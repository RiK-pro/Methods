import requests
import json
from pprint import pprint

token = '&access_token=6a8eb724b348c994c5886a54c285ea1d377b75834da2622ace0dd296e98d6358d559db91cbe087a79ac6b'
main_link = 'https://api.vk.com/method/'  # Ссылка на апи вконтакте
method = 'users.getSubscriptions?v=5.52'  # метод для запроса сообществ пользователя
response = requests.get(f'{main_link}{method}{token}')

if response.ok:
    j_data = response.json()
    pprint(j_data)
    with open('vkgroup.json', 'w') as write_f:
        json.dump(j_data, write_f)
else:
    print('Ошибка!')
