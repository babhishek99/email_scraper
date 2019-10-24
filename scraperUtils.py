from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import sys


def secondary_security(browser):
    try:
        button = browser.find_element_by_class_name("secondary-action")
        button.click()
    except Exception as e:
        pass


def input_locator(elements, field):
    elements = [element for element in elements if element.get_attribute("type") == "text"]
    for element in elements:
        if field in element.get_attribute("placeholder"):
            return element


def button_locator(elements, field):
    for element in elements:
        if field == element.get_attribute("data-control-name"):
            return element


def scrape(driver, url, excel_obj, company, page_limit=10):
    for page in range(2, page_limit + 1): #change to desired page range 
        page_url = ""
        if page == 1:
            page_url = url
        else:
            page_url = url + "&page=" + str(page)
        print("Scraping this URL: " + page_url)
        driver.get(page_url)
        time.sleep(2)
        
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/5);")
            while not page_has_loaded(driver):
                pass    
            source_code = driver.page_source
            soup = BeautifulSoup(source_code)
            names = soup.findAll("span", {"class" : "name actor-name"})
            titles_location = soup.findAll("span", {"dir" : "ltr"})
            titles = titles_location[::2]
        
        iterator = zip(names, titles)
        seen_names = set()
        for name, position in iterator:
            if name in seen_names:
                continue
            seen_names.add(name.contents[0])
            print(name.contents[0] + "--->" + position.contents[0])
            wb_act = excel_obj.workbook.active
            wb_act['A' + str(excel_obj.curr_row)] = name.contents[0]
            wb_act['B' + str(excel_obj.curr_row)] = position.contents[0]
            wb_act['C' + str(excel_obj.curr_row)] = company
            excel_obj.curr_row += 1
        
        excel_obj.saveFile()


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def execute(excel_obj, user_obj):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = "C:\\Users\\Abhishek\\AppData\\Local\\Google\\Chrome SxS\\Application\\chrome.exe"
    browser = None
    while True:
        try: 
            browser = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
            browser.implicitly_wait(30)
            browser.get("https://www.linkedin.com")
            browser.find_element_by_class_name("nav__button-secondary").click()
            username = browser.find_element_by_id("username")
            username.send_keys(user_obj.get_username())
            password = browser.find_element_by_id("password")
            password.send_keys(user_obj.get_password())
            password.submit()
            break
        except Exception as e:
            browser.close()

    # secondary_security(browser)
    for company in user_obj.get_companies():
        #FILTER PAGE
        browser.get("https://www.linkedin.com/search/results/people/?origin=DISCOVER_FROM_SEARCH_HOME")

        #ALL FILTERS BUTTON
        time.sleep(3)
        button_elements = browser.find_elements_by_tag_name("button")
        all_filters_button = button_locator(button_elements, "all_filters")
        all_filters_button.click()

        #ELEMENTS
        input_elements = browser.find_elements_by_tag_name("input")
        button_elements = browser.find_elements_by_tag_name("button")

        # FILTER LOCATIONS
        location_elem = input_locator(input_elements, "country/region")
        # locations = ["United States", "San Francisco Bay Area"]
        for location in user_obj.get_locations():
            location_elem.send_keys(location)
            time.sleep(1)
            location_elem.send_keys(Keys.DOWN)
            location_elem.send_keys(Keys.ENTER)
            time.sleep(1)

        #FILTER CURRENT COMPANY
        company_elem = input_locator(input_elements, "current company")
        company_elem.send_keys(company)
        time.sleep(1)
        company_elem.send_keys(Keys.DOWN)
        company_elem.send_keys(Keys.ENTER)
        time.sleep(1)

        #APPLY FILTERS
        apply_button = button_locator(button_elements, "all_filters_apply")
        apply_button.click()

        #BASE FILTER URL
        time.sleep(3)
        filter_url = browser.current_url
        print("Filter URL is: " + filter_url)

        #URL FOR EACH TITLE
        for title in user_obj.get_titles():
            title_url = filter_url + "&title=" + title
            scrape(browser, title_url, excel_obj, company)

    excel_obj.closeFile()
    print("Linkedin email scraping is complete.")
    print("Your file is located at this path from the current directory: " + path)