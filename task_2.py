import requests
import json

API_KEY = "d5307b331bf245e884dd530588f61c8a"
url = "https://api.weatherbit.io/v2.0/current"

params = {
    'key': 'd5307b331bf245e884dd530588f61c8a',
    'lang': 'ru',
    'units': 'M',
    'city': 'Moscow'
}

response = requests.get(url=url, params=params)
data = response.json()
with open('data_task2.json', 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)
