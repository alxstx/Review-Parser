from config_functions import *
import time
from bs4 import BeautifulSoup
import json

data = {'Отзыв': [], 'Оценка': [], 'Дата': [], 'Имя отправителя': []}
from config import informative_text


def button_clicker(url, driver):
    """
    Нажимать на кнопку чтобы увидеть все отзывы
    """
    driver.get(url)
    scroll_down(driver, 5)
    time.sleep(5)
    try:
        btn = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[1]/div[2]/div[6]/div/div[4]/a')
    except:
        btn = None
    if btn != None:
        btn.click()
    time.sleep(5)


def get_reviews(url):
    driver = create_driver()
    driver.get(url)
    if 'captcha' or 'showcaptcha' in driver.current_url:
        try:
            captcha(BeautifulSoup(driver.page_source, 'lxml'), driver)
        except:
            pass
    button_clicker(url, driver)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='comment-container-wrapper js-comment-container-wrapper')

    for item in items:
        if 'captcha' or 'showcaptcha' in driver.current_url:
            try:
               captcha(BeautifulSoup(driver.page_source, 'lxml'), driver)
            except:
                pass
        # получение текста
        try:
            review_text = item.find('span', 'js-comment-content').text
            review_text = review_text.replace('\xa0',' ')
        except:
            review_text = ['unknown']
        # получение кол. звезд
        try:
            thumbs_up = item.find('span', 'js-mark comment-thumb cursor pull-left mr15 plus').find_next('span',
                                                                                                        'mark-text').text
            thumbs_down = item.find('span', 'js-mark comment-thumb cursor pull-left mr15 minus').find_next('span',
                                                                                                           'mark-text').text
            stars = int(thumbs_up) - int(thumbs_down)
        except ArithmeticError:
            stars = 'unknown'
        # Получение даты
        try:
            date = item.find('span', 'iblock gray').text
            date = date.replace('\n', ' ').replace('\t', ' ').replace('через Foursquare','')
        except:
            date = 'unknown'
        # Получение имя отправителя
        try:
            name = item.find('span', 'name').text
            name = name.replace('\ue51c\ue052\ue314','')
        except:
            name = 'unknown'
        # Сохранить отзыв
        data['Отзыв'].append(''.join(review_text))
        data['Оценка'].append(stars)
        data['Дата'].append(date.strip())
        data['Имя отправителя'].append(name)


input(informative_text)
#  https://zoon.ru/msk/cinema/kinoteatr_formula_kino_v_severnom_chertanovo/
"""with open(input('Путь к json файлу с ссылками:')) as f:
    link_list = json.load(f)"""
link_list = ['https://zoon.ru/msk/cinema/kinoteatr_formula_kino_v_severnom_chertanovo/']
for link in link_list:
    get_reviews(link)

print(data)
"""with open(input('Выберите файл сохранения файлов в json'), 'w') as json_file:
  json.dump(data, json_file)"""
