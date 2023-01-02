import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
global url
url = "https://www.nba.com/stats/leaders"



def load_soup_elment():
    #Loading Soup object and return it
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def create_df_dict():
    #Creating a Dictionary for the Data Frame base on the Columns names and return it
    ID, Name, Team, GP, Minute, Points, FGM, FGA, FG_P = ([] for i in range(9))
    Three_PM, Three_PA, Three_Per, FTM, FTA, FT_P = ([] for i in range(6))
    OREB, DREB, REB, AST, STL, BLK, TOV, EFF, BIO = ([] for i in range(9))
    dict = {
        'ID':ID, 'Name':Name, 'Team':Team, 'GP':GP, 'Minute':Minute,
        'Points':Points, 'FGM':FGM, 'FGA':FGA, 'FG_P':FG_P, '3PM':Three_PM,
        '3PA':Three_PA, '3P%':Three_Per,'FTM':FTM, 'FTA':FTA, 'FT%':FT_P, 'OREB':OREB,
        'DREB':DREB, 'REB':REB, 'AST':AST, 'STL':STL, 'BLK':BLK, 'TOV':TOV, 'EFF':EFF, 'BIO':BIO
    }
    return dict

def bioInfo(playerUrl):
    #Input - Player page URL
    #Crawl to the url and return the BIO section(otherwise return non)
    driver.get('https://www.nba.com' + playerUrl)
    try:
        driver.find_element(By.LINK_TEXT, "Bio").click()
        bio=driver.find_element(By.CLASS_NAME, "PlayerBio_player_bio__kIsc_").text
    except :
        bio = "non"
    return bio


def getting_data():
    #Creating the Data Frame, crawl to each NBA Season and save the Stats Table to DF
    driver.get(url)
    dict = create_df_dict()
    df = pd.DataFrame(dict)
    for season_num in range(10):
        season = '20' + str(22 - season_num) + '-' + str(23 - season_num)
        season_select = Select(driver.find_element(By.CLASS_NAME, 'DropDown_select__4pIg9'))
        season_select.select_by_visible_text(season)
        time.sleep(2)
        page_drop = Select(driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select'))
        page_drop.select_by_visible_text("All")
        time.sleep(2)
        soup = load_soup_elment()
        rows = soup.find_all('tr')
        rows.pop(0)
        for row in rows:
            cells = row.find_all('td')
            row_num = len(df)
            player_row = []
            for index, value in enumerate(dict.values()):
                if(index != 23):
                    player_row.append(cells[index].text.strip())
                else:
                    player_row.append(bioInfo(cells[1].find('a')['href']))
            df.loc[row_num] = player_row
        df.to_csv('Data.csv')

        driver.get(url)
    df.to_csv('Data.csv')
    driver.quit()
    
getting_data()