import requests
from lxml import html
from bs4 import BeautifulSoup


url = 'https://dzen.ru'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.931 Yowser/2.5 Safari/537.36"
}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.content)


def parser_dzen_news(content_dom):
    news_container = content_dom.xpath("//div[contains(@class,'mg-card ')]")
    dzen_news = []
    for new_container in news_container:
        element = dict()
        news_name = new_container.xpath(".//h2/a/text()")
        element['name'] = str(news_name[0]).replace(u'\xa0', u' ')

        news_link = new_container.xpath(".//h2/a/@href")
        element['link'] = str(news_link[0])

        news_date = new_container.xpath(".//span[@class='mg-card-source__time']/text()")
        element['date'] = str(news_date[0]).strip()

        news_source = new_container.xpath(".//a[@class='mg-card__source-link']/text()")
        element['source'] = str(news_source[0])

        dzen_news.append(element)
    return dzen_news


print(parser_dzen_news(dom))
