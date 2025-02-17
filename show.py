import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys 
from main import main

def get_show_id(show_name):
    
    url = f"https://www.imdb.com/find/?q={show_name.replace(' ', '%20')}"
    
    os.environ["PATH"] += os.pathsep + r'C:\Users\samad\Downloads'
    driver = webdriver.Chrome()
    driver.get(url)
    
    show_name_element = driver.find_element(By.CLASS_NAME, "ipc-metadata-list-summary-item__t")
    show_url = show_name_element.get_attribute("href")
    show_id = show_url.split('/')[4]
    # print(show_id)
    return show_id
    
show_name = input("Enter a show name: ")
show_id = get_show_id(show_name)
main(show_id)