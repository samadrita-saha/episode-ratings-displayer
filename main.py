import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_num_seasons(show_id):   

    url = f"https://www.imdb.com/title/{show_id}"

    options = Options()
    options.add_argument('--headless=new')  
    options.add_argument('--window-size=1920x1080')  
    options.add_argument('--disable-blink-features=AutomationControlled')  
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    multi_season = driver.find_elements(By.XPATH, "//select[@id='browse-episodes-season']")
    # print(multi_season)
    
    if(len(multi_season) == 0):
        seasons = [1]
    else:
        xpath_expression = "//select[@id='browse-episodes-season']" 
        season_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_expression))
    )
        options = season_dropdown.find_elements(By.TAG_NAME, "option")    
        seasons = [int(option.text.strip()) for option in options if option.text.strip().isdigit()]
    # print(seasons)

    driver.quit()
    return max(seasons)


def get_episode_ratings(show_id, num_seasons):
    
    episode_data = []

    options = Options()
    options.add_argument('--headless=new')  
    options.add_argument('--window-size=1920x1080')  
    options.add_argument('--disable-blink-features=AutomationControlled')  
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    service = Service(ChromeDriverManager().install())

    for season in range(1, num_seasons + 1):
        url = f"https://www.imdb.com/title/{show_id}/episodes/?season={season}"

        driver = webdriver.Chrome(service=service, options=options)
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
                episode_rating = None
            
            match_10 = re.search(r'(\d\d+)\s*(?=/10)', episode_blurb)
            if match_10:
                episode_rating = "10"

            episode_data.append({
                "Season": season,
                "Episode": i+1,
                "Rating": episode_rating
            })
  
    driver.quit()  
    return episode_data


def generate_heatmap(df, show_title):
    
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    heatmap_data = df.pivot(index='Episode', columns='Season', values='Rating')
    heatmap_data.dropna(axis=0, how='all', inplace=True)
    heatmap_data.dropna(axis=1, how='all', inplace=True)

    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_data, annot=True, cmap="RdYlGn", linewidths=0.5, fmt=".1f", center=5.0, vmin=0, vmax=10)
    plt.gca().xaxis.set_label_position('top')  
    plt.gca().xaxis.tick_top()  
    plt.xlabel('Season')
    plt.ylabel('Episode')
    plt.title(show_title)
    # plt.show()

    image_filename = "heatmap.png"
    image_path = os.path.join('static', image_filename)
    plt.savefig(image_path)
    plt.close()

    return image_filename 

           
# def main(show_id):
#     num_seasons = get_num_seasons(show_id)
#     episode_data = get_episode_ratings(show_id, num_seasons)
#     df = pd.DataFrame(episode_data)
#     print(df)
#     generate_heatmap(df)


# if __name__ == "__main__":
#     # show_id = "tt7366338" # Chernobyl
#     show_id = "tt7120662" # Derry Girls
#     main(show_id)