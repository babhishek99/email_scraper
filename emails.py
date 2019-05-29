#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from selenium import webdriver
from tqdm import tqdm
import re
from selenium.webdriver.support.ui import WebDriverWait
import openpyxl
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains


#Company list can be imported from excel or hardcoded as a list
company_lst = list(pd.read_excel("Company List.xlsx")['Company'])
#Change this list according to titles you want to scrape for
titles = ["Manager", "Director"]

#Assigning active excel notebook change path accordingly
workbook = openpyxl.Workbook()
path = "Sourcing - Abs.xlsx"
wb_act = workbook.active
curr_row = 2

#LINKEDIN AUTHENTICATION

username_auth = input("Enter your Linkeden username: ")
password_auth = input("Enter your Linkeden password: ")

while True:
    try: 
        browser = webdriver.Chrome('chromedriver.exe')
        browser.implicitly_wait(30)
        browser.get("https://www.linkedin.com")
        browser.find_element_by_class_name("nav__button-secondary").click()
        username = browser.find_element_by_id("username")
        username.send_keys(username_auth)
        password = browser.find_element_by_id("password")
        password.send_keys(password_auth)
        password.submit()
        break
    except Exception as e:
        browser.close()


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


def scrape(driver, url, row, company, page_limit=2):
    for page in range(1, page_limit + 1): #change to desired page range 
        page_url = ""
        if page == 1:
            page_url = url
        else:
            page_url = title_url + "&page=" + str(page)
        print("Scraping this URL: " + page_url)
        driver.get(page_url)
        time.sleep(2)
        
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/5);")
            while not page_has_loaded(browser):
                pass    
        
        source_code = driver.page_source
        soup = BeautifulSoup(source_code)
        iterator = zip(soup.findAll("span", {"class" : "name actor-name"}), soup.findAll("span", {"dir" : "ltr"}))
        for name, position in iterator:
            print(name.contents[0] + "--->" + position.contents[0])
            wb_act['A' + str(row)] = name.contents[0]
            wb_act['B' + str(row)] = position.contents[0]
            wb_act['C' + str(row)] = company
            row += 1
        
        workbook.save(path)
        
        return row


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

# Use the below line if Linkeden asks for secondary security such as adding a phone number
# secondary_security(browser)

for company in company_lst:
    #FILTER PAGE
    browser.get("https://www.linkedin.com/search/results/people/?origin=DISCOVER_FROM_SEARCH_HOME")

    #ALL FILTERS BUTTON
    button_elements = browser.find_elements_by_tag_name("button")
    all_filters_button = button_locator(button_elements, "all_filters")
    all_filters_button.click()

    #ELEMENTS
    input_elements = browser.find_elements_by_tag_name("input")
    button_elements = browser.find_elements_by_tag_name("button")

    # FILTER LOCATIONS
    location_elem = input_locator(input_elements, "location")
    locations = ["United States", "San Francisco Bay Area"]
    for location in locations:
        location_elem.send_keys(location)
        time.sleep(1)
        location_elem.send_keys(Keys.RETURN)
        time.sleep(1)

    #FILTER CURRENT COMPANY
    company_elem = input_locator(input_elements, "current company")
    company_elem.send_keys(company)
    time.sleep(1)
    company_elem.send_keys(Keys.RETURN)
    time.sleep(1)

    #APPLY FILTERS
    apply_button = button_locator(button_elements, "all_filters_apply")
    apply_button.click()

    #BASE FILTER URL
    time.sleep(3)
    filter_url = browser.current_url
    print("Filter URL is: " + filter_url)

    #URL FOR EACH TITLE
    for title in titles:
        title_url = filter_url + "&title=" + title
        curr_row = scrape(browser, title_url, curr_row, company)


