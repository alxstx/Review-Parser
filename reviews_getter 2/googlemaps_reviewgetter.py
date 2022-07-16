import json
import time
from config_functions import create_driver,scroll_down,captcha
from bs4 import BeautifulSoup
def click_capt(driver):
    scroll_down(driver,4)
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span').click()

def getReview(placename):
    reviewListFile = open("review.txt", "w", encoding='UTF-8')
    resultJSON = []
    driver = create_driver()
    driver.get("https://www.google.com/maps")
    if 'captcha' or 'showcaptcha' in driver.current_url:
        captcha(BeautifulSoup(driver.page_source,'lxml'),driver)
    click_capt(driver)
    time.sleep(12)
    KEYWORDS = placename
    # Найти в гугле место
    searchbox = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    searchbox.send_keys(KEYWORDS)

    searchbutton = driver.find_element_by_css_selector("button#searchbox-searchbutton")
    searchbutton.click()

    time.sleep(5)

    try:
       reviewbutton = driver.find_element_by_css_selector("button.gm2-button-alt.HHrUdb-v3pZbf")
       reviewbutton.click()
    except:
        pass

    time.sleep(7)

    try:
        reviewElement = driver.find_elements_by_css_selector(
            "#pane > div.widget-pane > div.widget-pane-content > div.widget-pane-content-holder > div.section-layout > div.section-layout.section-scrollbox > div.section-layout")[
            3]
    except IndexError:
        try:
           reviewElement = driver.find_elements_by_css_selector(
            "#pane > div.widget-pane > div.widget-pane-content > div.widget-pane-content-holder > div.section-layout > div.section-layout.section-scrollbox > div.section-layout")[
            2]
        except IndexError:
            try:
               reviewElement = driver.find_elements_by_css_selector(
                "#pane > div.widget-pane > div.widget-pane-content > div.widget-pane-content-holder > div.section-layout > div.section-layout.section-scrollbox > div.section-layout")[
                1]
            except IndexError:
                reviewElement = driver.find_elements_by_css_selector(
                    "#pane > div.widget-pane > div.widget-pane-content > div.widget-pane-content-holder > div.section-layout > div.section-layout.section-scrollbox > div.section-layout")[
                    0]


    previousLastReview = None
    items = driver.find_elements_by_class_name('button')
    for item in items:
        driver.execute_script('arguments[0].scrollIntoView(true);', item)
        item.click()
    # Получить все отзывы
    while True:
        if 'captcha' or 'showcaptcha' in driver.current_url:
            captcha(BeautifulSoup(driver.page_source, 'lxml'), driver)
        time.sleep(2)
        reviews = reviewElement.find_elements_by_xpath("//div[contains(@data-review-id, 'Ch')]")
        lastReview = reviews[-1]
        driver.execute_script('arguments[0].scrollIntoView(true);', lastReview)
        if previousLastReview != lastReview:
            previousLastReview = lastReview
        else:
            break
    # Получить все данные из отзывов и сохранить их в json
    for c in reviews:
        if 'captcha' or 'showcaptcha' in driver.current_url:
            captcha(BeautifulSoup(driver.page_source, 'lxml'), driver)
        reviewer = c.get_attribute("aria-label")
        message = c.find_elements_by_css_selector("div.ODSEW-ShBeI-ShBeI-content > span")[1].get_attribute('innerHTML')
        ratings = c.find_element_by_css_selector("span.ODSEW-ShBeI-H1e3jb").get_attribute('aria-label')
        data = c.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[10]/div[28]/div/div[3]/div[3]/div[1]/span[3]').text
        if reviewer is not None:
            print({"Имя отправителя": reviewer, "Оценка": ratings, "Отзыв": message,'Дата':data})
            resultJSON.append({"Имя отправителя": reviewer, "Оценка": ratings, "Отзыв": message,'Дата':data})

    resultJSON = {"result": resultJSON}
    resultJSON = json.dumps(resultJSON, ensure_ascii=False)
    print(resultJSON)
    reviewListFile.write(resultJSON)

    reviewListFile.close()
    driver.close()

with open(input('Путь к json файлу с ссылками:')) as f:
    places = json.load(f)

places = ['Гум Москва']
for place in places:
    getReview(place)

