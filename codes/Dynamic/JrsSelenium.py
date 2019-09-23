# -*- coding: utf-8 -*-
from selenium import webdriver

if __name__ == "__main__":
    drive = webdriver.Chrome()
    drive.get('http://192.168.0.103:8000/places/default/search')
    drive.find_element_by_id('search_term').send_keys('.')
    js = "document.getElementById('page_size').options[1].text='1000'"
    drive.execute_script(js)
    drive.find_element_by_id('search').click()
    drive.implicitly_wait(30)
    links = drive.find_elements_by_css_selector('#results a')
    countries = [link.text for link in links]
    print countries
    drive.close()

