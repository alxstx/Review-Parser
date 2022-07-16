import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from anticaptchaofficial.imagecaptcha import *


def create_driver():
    """
    Создавание драйвера с функцией antiseleniumdetect чтобы сайт не понял что бот а не человек находиться на сайте
    """
    print('creating driver')
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    #options.headless = True # убрать комментирование если не хотите видеть окно - но это может привести к ошибкам
    driver = webdriver.Chrome(options=options,
                              executable_path='/Users/alex/PycharmProjects/reviews_getter/chromedriver1')  # тут изменить путь
    print('created driver')
    return driver


def scroll_down(driver, n):
    """
    скролл вниз по сайту - n= сколько надо скроллнуть вниз
    """
    html = driver.find_element_by_tag_name('html')
    for i in range(n):
        html.send_keys(Keys.PAGE_DOWN)


def get_html2(url, driver):
    """
    Перейти на сайт и получить html код
    """
    try:
        driver.get(url)
        html = driver.page_source
    except:
        html = ''
        pass
    return html


def captcha(soup, driver):
    """
    Пройти каптчу
    """
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key("8040f6428458d0426cc2c520d99674b9")
    link = soup.find('img').get('href')
    print(link)
    if link != None:
        photo = urllib.request.urlretrieve(link, f'{link}.jpg')
        inputt = driver.find_element_by_tag_name('input')
        captcha_text = solver.solve_and_return_solution(f'{link}.jpg')
        inputt.send_keys(captcha_text)
        btn = driver.find_element_by_tag_name('button')
        btn.click()
        if captcha_text != 0:
            print("captcha text " + captcha_text)
        else:
            print("task finished with error " + solver.error_code)


def x_path(element):
    """
    Получение xpath из тэга html кода (может не пригодиться)
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
            )
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)
