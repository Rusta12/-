'''
2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД. Магазины можно
выбрать свои. Главный критерий выбора: динамически загружаемые товары
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

import time
from pprint import pprint


chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get('https://www.mvideo.ru')

goods_data = []

time.sleep(1)
n = 0
while True:
    try:
        city = driver.find_element_by_xpath("//a[@class='btn btn-approve-city'][@href]")
        city.click()
        city.send_keys(Keys.ENTER)
        break
    except:
        if n == 5:
            break
        else:
            n += 1

time.sleep(2)

button = driver.find_element_by_xpath("//div[@class='main-holder sel-main-holder']//div[7]")
button.click()

n = 0
time.sleep(2)
while True:
    try:
        time.sleep(2)
        data = button.find_elements_by_xpath(".//li[@class='gallery-list-item height-ready']")
        t = 0
        for good in data:
            goods = {}

            a = good.find_element_by_xpath(".//h4")
            goods['name'] = a.get_attribute('title')

            b = good.find_element_by_class_name('sel-product-tile-title')
            goods['link'] = b.get_attribute('href')

            c = good.find_element_by_class_name('c-pdp-price__current').text
            goods['old_price'] = str(c).replace('¤','')

            try:
                d = good.find_element_by_xpath(".//span[@class='u-font-bold c-pdp-price__trade-price']").text
                goods['new_price'] = str(d).replace('¤','')
            except:
                goods['new_price'] = None

            e = good.find_element_by_class_name('c-pdp-price__monthly').text
            goods['monthly_payment'] = str(e).replace('¤','руб')

            goods['raiting'] = good.find_element_by_class_name('c-star-rating_reviews-qty').text

            if (goods['old_price'] != '') and (goods['raiting']) != '':
                goods_data.append(goods)
                t += 1

        bclick = button.find_element_by_xpath(".//a[@class='next-btn sel-hits-button-next'][@href]")
        bclick.click()
        n += 1
    except:
        break


pprint(goods_data)
driver.quit()

client = MongoClient('localhost', 27017)
db = client['goods_db']
goods_get = db.goods_db

