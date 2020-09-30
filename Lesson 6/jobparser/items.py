# -*- coding: utf-8 -*-
# Define here the models for your scraped items
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):       # Создаем структуру item'a
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    link = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    company = scrapy.Field()
    currency = scrapy.Field()
    site = scrapy.Field()
