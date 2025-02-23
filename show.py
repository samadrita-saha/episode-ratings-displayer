import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

# from main import main
from utils import create_driver


def get_show_info(show_name):

    url = f"https://www.imdb.com/find/?q={show_name.replace(' ', '%20')}"

    driver = create_driver()
    driver.get(url)

    show_name_element = driver.find_element(
        By.CLASS_NAME, "ipc-metadata-list-summary-item__t"
    )
    show_url = show_name_element.get_attribute("href")
    show_id = show_url.split("/")[4]
    show_title = show_name_element.text
    # print(show_id)

    driver.quit()
    return show_id, show_title


# show_name = input("Enter a show name: ")
# show_id = get_show_id(show_name)
# main(show_id)
    
# show_name = input("Enter a show name: ")
# show_id, show_title = get_show_info(show_name)
# print(show_title, show_id)
# main(show_id)