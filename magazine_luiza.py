# -*- encoding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import json
import time

url_magazine_luiza = "https://www.magazineluiza.com.br/"


def getProducts(str_search_product):

    # WEBDRIVER SETUP
    options = Options()
    options.headless = False
    user_agent = getRamdomUserAgent()
    options.add_argument("user-agent={}".format(user_agent))
    driver = webdriver.Firefox(options=options)

    driver.get(url_magazine_luiza)
    driver.implicitly_wait(10)

    # SEARCH SETUP
    input_element = driver.find_element_by_id('inpHeaderSearch')
    input_element.clear()
    input_element.send_keys(str_search_product)
    driver.find_element_by_id('btnHeaderSearch').click()
    print('Current product: ' + str_search_product)

    # driver.implicitly_wait(10)
    myElem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'nm-price-container')))

    # SEARCH PROCESS
    def searchProcess():
        search_results = driver.find_element_by_class_name(
            'nm-search-results-container')
        tablets = search_results.find_elements_by_xpath(
            "//li[contains(@class, 'nm-product-item')][not(contains(@class, 'hide-priceapi'))]")

        for tablet in tablets:
            tablet_name = tablet.find_element_by_class_name('nm-product-name')
            tablet_price = tablet.find_element_by_class_name(
                'nm-price-container')
            print(tablet_name.text.strip())
            print(tablet_price.text.strip())

    searchProcess()

    page = 1

    while True:

        try:

            page = page + 1

            print("\n\nPAGINA: {}\n\n".format(page))

            next_page = driver.find_element_by_xpath(
                "//a[@title='Ir para a página {}']".format(page)).click()

            myElem = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'nm-price-container')))

            time.sleep(3)

            # driver.implicitly_wait(15)

            searchProcess()

        except:
            driver.quit()
            break


def getRamdomUserAgent():
    software_names = [SoftwareName.FIREFOX.value]
    operating_systems = [OperatingSystem.WINDOWS.value,
                         OperatingSystem.LINUX.value]

    user_agent_rotator = UserAgent(
        software_names=software_names, operating_systems=operating_systems, limit=100)

    user_agents = user_agent_rotator.get_user_agents()
    user_agent = user_agent_rotator.get_random_user_agent()
    print(user_agent)

    return user_agent


# getProducts('Tablet Samsung')
# getProducts('geladeira frost free brastemp inverse')
getProducts('geladeira')
