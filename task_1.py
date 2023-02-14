import requests
from prettytable import PrettyTable
import json

table = PrettyTable()
table.field_names = ["Key", "Value"]

github_username = "TemirOrig"
api_url = f"https://api.github.com/users/{github_username}/repos"
response = requests.get(api_url)
data = response.json()
for repository in data:
    print(repository["name"])

# for repository in data:
#     table.add_row([repository["name"], repository["created_at"]])
# print(table)
# блок кода для вывода таблицы с репозиториями и датой их создания

# with open('data_task1.json', 'w', encoding='utf-8') as output_file:
#     json.dump(data, output_file, ensure_ascii=False, indent=4)
# блок кода, для создания и сохранения .json файла

