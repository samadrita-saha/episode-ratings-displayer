import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_num_seasons_with_selenium(show_id):   

    url = f"https://www.imdb.com/title/{show_id}"
    
    os.environ["PATH"] += os.pathsep + r'C:\Users\samad\Downloads'
    driver = webdriver.Chrome()
    driver.get(url)
    
    xpath_expression = "//select[@id='browse-episodes-season']"
    season_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_expression))
    )
    options = season_dropdown.find_elements(By.TAG_NAME, "option")    
    seasons = [int(option.text.strip()) for option in options if option.text.strip().isdigit()]
    
    return max(seasons) if seasons else None


show_id = "tt0903747"  
num_seasons = get_num_seasons_with_selenium(show_id)
print(f"Number of seasons: {num_seasons}")