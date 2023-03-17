import scrapy
from scrapy.http import HtmlResponse


class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://spb.hh.ru/search/vacancy?area=2&ored_clusters=true&text=Python&search_period=1&page=1"
    ]

    def parse(self, response:HtmlResponse, **kwargs):
        print('\n_______________________________\n%s\n_________________________________\n'%response.url)
