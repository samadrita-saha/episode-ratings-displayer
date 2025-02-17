import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd

def get_num_seasons(show_id):   

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
    # print(max(seasons))

    driver.quit()
    return max(seasons) if seasons else None


def get_episode_ratings(show_id, num_seasons):
    
    episode_data = []

    for season in range(1, num_seasons + 1):
        url = f"https://www.imdb.com/title/{show_id}/episodes/?season={season}"

        os.environ["PATH"] += os.pathsep + r'C:\Users\samad\Downloads'
        driver = webdriver.Chrome()
        driver.get(url)
        
        episodes = driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-f2169d65-1 iwjtYd')]")
        # print(f"Number of episodes: {len(episodes)}")
        
        for i in range(len(episodes)):
            episode_blurb = episodes[i].text.strip()
            # print(episode_blurb)
            
            match = re.search(r'(\d+\.\d+)\s*(?=/10)', episode_blurb)
            if match:
                episode_rating = match.group(1)  
            else:
                episode_rating = "No Rating"  
            
            episode_data.append({
                "Season": season,
                "Episode": i+1,
                "Rating": episode_rating
            })
  
    driver.quit()  
    return episode_data
           

def main(show_id):
    
    num_seasons = get_num_seasons(show_id)
    episode_data = get_episode_ratings(show_id, num_seasons)
    
    df = pd.DataFrame(episode_data)
    print(df)


show_id = "tt7120662" 
main(show_id)