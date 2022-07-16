from yandex_classes import Review
import time
from config_functions import create_driver,captcha
import json
from bs4 import BeautifulSoup


data = {'Отзыв': [], 'Оценка': [], 'Дата': [], 'Имя отправителя': []}
review_dicts = []

driver = create_driver()


def parser_reviews(url,
                   driver):
    driver.get(
        url
    )
    # Получить все кнопки "еще"
    more_buttons = driver.find_elements_by_xpath(
        '//*[@class="business-review-view__expand"]'
    )
    # Проверить на наличие каптчи и пройти если есть
    if 'captcha' or 'showcaptcha' in driver.current_url:
        try:
           soup = BeautifulSoup(driver.page_source,'lxml')
           captcha(soup,driver)
        except:
            pass
    # Нажать на все кнопки еще
    for more_button in more_buttons:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", more_button)
            print('done')
        except:
            pass
    if 'captcha' or 'showcaptcha' in driver.current_url:
        try:
            captcha(BeautifulSoup(driver.page_source, 'lxml'), driver)  # Проверка наличии каптчы
        except:
            pass
    # получить все отзывы
    reviews = driver.find_elements_by_xpath('//*[@class="business-review-view__info"]')
    print("Отзывов найденно: {}".format(len(reviews)))
    # прокрутить все отзывы через класс который парсит все элементы
    for review in reviews:
        if 'captcha' or 'showcaptcha' in driver.current_url:
            captcha(BeautifulSoup(driver.page_source, 'lxml'), driver)
        driver.execute_script("arguments[0].scrollIntoView(true);", review)
        review_dicts.append(Review(review).__dict__)
    driver.close()


# Пример как должна выглядеть ссылка: 'https://yandex.ru/maps/org/yandeks/1124715036/reviews/?ll=37.588144%2C55.733842&z=16'
"""with open(input('Путь к json файлу с ссылками:')) as f:
    link_list = json.load(f)"""
link_list = ['https://yandex.ru/maps/org/yandeks/1124715036/reviews/?ll=37.588144%2C55.733842&z=16']
for link in link_list:
    parser_reviews(link, driver)
for rev in review_dicts:
    data['Имя отправителя'].append(rev['author_name'])
    data['Отзыв'].append(rev['text'])
    data['Оценка'].append(rev['stars'])
    data['Дата'].append(str(rev['datetime']))
print(data)
"""with open(input('Выберите файл сохранения файлов в json'), 'w') as json_file:
    json.dump(data, json_file)"""
