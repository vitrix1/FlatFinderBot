from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
from datetime import datetime

URL = 'https://nsk.besposrednika.ru/'

PARAMS = {'Комнаты':
               {'Студия': 'field_category_3000',
                'Комната': 'field_category_1000',
                'Дом': 'field_category_2000',
                'Однокомнатная квартира': 'field_category_1',
                'Двухкомнатная квартира': 'field_category_2',
                'Трёхкомнатная квартира': 'field_category_3',
                'Четырёхкомнатная квартира': 'field_category_4',
                'Подселение': 'field_podselenie_da'},

          'Цена_от': 'priceInputFrom',
          'Цена_до': 'priceInputTo',

          'Город': ['Новосибирск', 'Бердск', 'Обь', 'Краснообск', 'Кольцово']}


async def parser(data_from_user):
    # service = Service(executable_path="driver/chromedriver.exe")
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(URL)
        # driver.fullscreen_window()
        for key, value in data_from_user.items():
            if key == 'Комнаты' and value != None:
                driver.find_element(By.ID, PARAMS[key][value]).click()
            elif (key == 'Цена_от' or key == 'Цена_до') and value != None:
                driver.find_element(By.ID, PARAMS[key]).send_keys(value)
            elif key == 'Город' and value != None:
                Select(driver.find_element(By.ID, "field_city")).select_by_visible_text(value)
        driver.find_element(By.NAME, 'Submit').click()
        result = bs(driver.page_source, features='html.parser')
        if result.find_all(class_='sEnLiCell unavailable'):
            links = {}
            for link in result.find_all(class_='sEnLiCell unavailable'):
                links[link.find('a')['href']] = link.find('a').text
            return links
        else:
            return
    except Exception as error:
        with open('log.txt', 'a') as file:
            file.write(f'{datetime.now()} {error}\n')
    finally:
        driver.close()
        driver.quit()

if __name__ == '__main__':
    data = {'Комнаты':'Студия', 'Цена_от':15000, 'Цена_до': 25000, 'Город': 'Новосибирск'}
    res = parser(data)
