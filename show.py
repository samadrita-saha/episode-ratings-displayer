import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# from main import main

def get_show_info(show_name):
    
    url = f"https://www.imdb.com/find/?q={show_name.replace(' ', '%20')}"

    options = Options()
    options.add_argument('--headless=new')  
    options.add_argument('--window-size=1920x1080')  
    options.add_argument('--disable-blink-features=AutomationControlled')  
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    # show_name_element = driver.find_element(By.CLASS_NAME, "ipc-metadata-list-summary-item__t")
    show_name_element = driver.find_element(By.XPATH, "//li[contains(@class, 'find-result-item')]//a")
    show_url = show_name_element.get_attribute("href")
    show_id = show_url.split('/')[4]
    show_title = show_name_element.text
    # print(show_id)
    
    return show_id, show_title

    
# show_name = input("Enter a show name: ")
# show_id, show_title = get_show_info(show_name)
# print(show_title, show_id)
# main(show_id)