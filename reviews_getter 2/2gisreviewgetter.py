from selenium import webdriver
from config_functions import *
import time
from bs4 import BeautifulSoup
import json

data = {'Отзыв': [], 'Оценка': [], 'Дата': [], 'Имя отправителя': []}
from config import informative_text


def button_clicker(url, driver):
    """
    нажатие на кнопку все отзывы
    """
    driver.get(url)
    scroll_down(driver, 3)
    for i in range(10):
        try:
            btn = driver.find_element_by_tag_name('button__label button__label js-button-label loader-holder__content')
        except:
            btn = None
        if btn != None:
            btn.click()
        scroll_down(driver, i + 3)


def get_reviews(url):
    driver = create_driver()
    driver.get(url)
    # button_clicker(url, driver)
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div[3]/div[1]').click()
    html1 = driver.page_source
    soup1 = BeautifulSoup(html1, 'lxml')
    for i in range(int(soup1.find('span','_18lf326a').text)):
        scroll_down(driver,1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    xathnss = soup.find_all('span', '_17ww69i')
    for xp in xathnss:
        try:
            xath = x_path(xp)
        except:
            xath = ''
        if xath != '':
            try:
                btnn = driver.find_element_by_xpath(xath)
            except:
                btnn = None
            driver.execute_script('arguments[0].scrollIntoView(true);', btnn)
            if btnn != None:
                driver.execute_script("arguments[0].click();", btnn)
    items = soup.find_all('div', class_='_yqieuf')
    review_text = []
    for item in items:
        if 'captcha' or 'showcaptcha' in driver.current_url:
            try:
                captcha(BeautifulSoup(driver.page_source, 'lxml'), driver)  # Проверка наличии каптчы
            except:
                pass
        # получение текста
        try:
            reviews = item.find('div', class_='_49x36f')
            review_text = reviews.find_next('a').text
        except:
            review_text = 'unknown'
        # получение кол. звезд
        try:
            all_stars = item.find_all('svg')
            dop_list = []
            for star in all_stars:
                if star.get('fill') == '#ffb81c':
                    dop_list.append('stars')
            stars = len(dop_list)
        except:
            stars = 'unknown'
        # Получение даты
        try:
            date = item.find('div', '_4mwq3d').text
        except:
            date = 'unknown'
        # Получение имя отправителя
        try:
            name = item.find('span', '_16s5yj36').text
        except:
            name = 'unknown'
        # Сохранить отзыв
        data['Отзыв'].append(review_text)
        data['Оценка'].append(stars)
        data['Дата'].append(date)
        data['Имя отправителя'].append(name)


input(informative_text)
# Получить ссылки из json файла
"""with open(input('Путь к json файлу с ссылками:')) as f:
    link_list = json.load(f)"""
# Парсинг
link_list = ['https://2gis.ru/novosibirsk/firm/141265769365151/tab/reviews?m=82.897524%2C54.981412%2F16']
for link in link_list:
    get_reviews(link)

print(data)
# Сохранение данных в json файл
with open(input('Выберите файл сохранения файлов в json'), 'w') as json_file:
    json.dump(data, json_file)
