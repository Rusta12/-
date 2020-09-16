"""
Урок 4. Парсинг HTML. XPath
Cобираем новости с сайтов news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath.
- название источника;
- наименование новости;
- ссылку на новость;
- дата публикации.
"""

from lxml import html
from pprint import pprint
import requests
import datetime
from pymongo import MongoClient

now = datetime.datetime.now()


class news():
    def __init__(self):
        self.__header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
                         'Accept': '*/*'}
        self.__mlink = 'https://news.mail.ru'
        self.__llink = 'https://lenta.ru'
        self.__ylink = 'https://yandex.ru'

        self.__news = []

    @staticmethod
    # парсинг новостной страницы mail
    def __parse_mail_news(self, link):
        response = requests.get(self.__mlink + link, headers=self.__header)
        dom = html.fromstring(response.text)
        news = {}
        head = dom.xpath("//h1/text()")[0]
        url = self.__mlink + link
        raw_time = \
        dom.xpath("//div[@class='cols__inner']/div[contains(@class,'article')]/div[1]/span[1]/span/span/@datetime")[0]
        source = dom.xpath("//div[@class='cols__inner']/div[contains(@class,'article')]/div[1]/span[2]/span/a/@href")[0]
        news['header'] = head
        news['source'] = source
        news['url'] = url
        news['time'] = raw_time
        news['parse_time'] = now.strftime("%Y-%m-%d %H:%M")
        news['_id'] = hash(news['url'])
        self.__news.append(news)

    # функция парсинга новостей mail
    def parse_mail(self):
        response = requests.get(self.__mlink, headers=self.__header)
        dom = html.fromstring(response.text)
        news_blocks = dom.xpath("//div[contains(@class,'daynews__item')]/a/@href")
        for block in news_blocks:
            self.__parse_mail_news(self, block)

    # функция парсинга новостей lenta.ru
    def parse_lenta(self):
        response = requests.get(self.__llink, headers=self.__header)
        dom = html.fromstring(response.text)
        f_news = {}
        news_block = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']/.//div[@class='item']")
        first_news = dom.xpath(
            "//section[@class='row b-top7-for-main js-top-seven']/.//div[contains(@class,'first-item')]")
        f_news['header'] = first_news[0].xpath("./h2/a/text()")[0]
        f_news['url'] = self.__llink + first_news[0].xpath("./h2/a/@href")[0]
        f_news['time_raw'] = first_news[0].xpath("./h2/a/time/@datetime")[0]
        f_news['source'] = self.__llink
        f_news['parse_time'] = now.strftime("%Y-%m-%d %H:%M")
        f_news['_id'] = hash(f_news['url'])
        self.__news.append(f_news)

        for block in news_block:
            news = {}
            news['header'] = block.xpath("./a/text()")[0]
            news['url'] = self.__llink + block.xpath("./a/@href")[0]
            news['time_raw'] = block.xpath("./a/time/@datetime")[0]
            news['source'] = self.__llink
            news['parse_time'] = now.strftime("%Y-%m-%d %H:%M")
            news['_id'] = hash(news['url'])
            self.__news.append(news)

    @staticmethod
    # парсинг новостной страницы mail
    def __parse_yandex_news(self, block):
        news = {}
        head = block.xpath(".//h2/a/text()")[0]
        url = self.__ylink + block.xpath(".//h2/a/@href")[0]
        raw_time = block.xpath(".//div[@class='story__date']/text()")[0]
        source = block.xpath(".//div[@class='story__date']/text()")[0]
        news['header'] = head
        news['source'] = source
        news['url'] = url
        news['time_raw'] = raw_time
        news['parse_time'] = now.strftime("%Y-%m-%d %H:%M")
        news['_id'] = hash(news['url'])
        self.__news.append(news)

    # функция парсинга новостей yandex
    def parse_yandex(self):
        # some code
        response = requests.get(self.__ylink + '/news', headers=self.__header)
        dom = html.fromstring(response.text)
        news_bloks = dom.xpath("//td[contains(@class,'stories-set__item')]")
        for block in news_bloks:
            self.__parse_yandex_news(self, block)

    def print_news(self):
        pprint(self.__news)

    def store_to_db(self):
        client = MongoClient('10.0.0.85', 27017)
        db = client['news_db']
        c_news = db.news
        for n in self.__news:
            c_news.update_one({'_id': n['_id']}, {'$set': n}, upsert=True)
            print('added' + str(n['_id']))


n = news()
n.parse_mail()
n.parse_lenta()
n.parse_yandex()
n.print_news()
