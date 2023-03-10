from pymongo import MongoClient
import requests
import fake_useragent
from bs4 import BeautifulSoup
import time
import json


client = MongoClient('localhost', 27017)
db = client['fresh_vac_db']
hh_vac = db.hh_vac


def get_links(text, num_of_pages, period):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f'https://spb.hh.ru/search/vacancy?area=2&ored_clusters=true&text={text}&search_period={period}&page=1',
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    if num_of_pages == 0:
        try:
            page_count = int(soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
        except:
            return
    else:
        page_count = num_of_pages
    for page in range(page_count):
        try:
            data = requests.get(
                url=f'https://spb.hh.ru/search/vacancy?area=2&ored_clusters=true&text={text}&search_period={period}&page={page}',
                headers={"user-agent": ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")
        time.sleep(1)


def get_vacancy(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        name = soup.find(attrs={"class":"bloko-header-section-1"}).text
    except:
        name = ""
    try:
        salary = soup.find(attrs={"class": "bloko-header-section-2 bloko-header-section-2_lite"}).text.replace("\xa0", "")
    except:
        salary = ""
    try:
        experience = soup.find(attrs={"class": "vacancy-description-list-item"}).find("span").text
    except:
        experience = ""
    vacancy = {
        "Вакансия": name,
        "Зарплата": salary,
        "Опыт работы": experience,
        "Ссылка на вакансию": link,
        "Ссылка на сайт": "https://spb.hh.ru"
    }
    return vacancy
    pass


def json_to_mongo(file, db_collection):
    with open(file, "r", encoding="utf-8") as data_file:
        json_data = data_file.read()
        json_data = json.loads(json_data)

    for item in json_data:
        db_collection.insert_one(item)


if __name__ == '__main__':
    data = []
    for a in get_links(input("Вакансия: "), int(input("Количество страниц(0 для всех доступных страниц): ")),
                       int(input("Введите период поиска(1, 3, 7 или 30): "))):
        data.append(get_vacancy(a))
        time.sleep(1)
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    json_to_mongo("data.json", hh_vac)
