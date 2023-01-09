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
statsUrl = "https://www.nba.com/stats/leaders"


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
        bio = driver.find_element(By.CLASS_NAME, "PlayerBio_player_bio__kIsc_").text
    except :
        bio = "non"
    return bio

def get_all_star_data():
    players = []
    for seasonNum in range(10):
        season = str(2022 - seasonNum)
        allStarUrl = 'https://www.basketball-reference.com/allstar/NBA_' + str(season) + '.html'
        driver.get(allStarUrl)
        soup = load_soup_elment()
        time.sleep(2)
        seasonPlayers = []
        playersTags = soup.find_all('th', attrs={'scope':'row', 'class':'left', 'data-stat':'player'})
        for tag in playersTags:
            try:
                Name = tag.find('a').text
                if Name not in players:
                    players.append(Name)
            except:
                continue

    df = pd.DataFrame({'Player Name':players})
    df.to_csv('All-Star Players.csv')

    




def getting_data():
    #Creating the Data Frame, crawl to each NBA Season and save the Stats Table to DF
    driver.get(statsUrl)
    dictToDF = create_df_dict()
    df = pd.DataFrame(dictToDF)
    for seasonNum in range(10):
        season = '20' + str(22 - seasonNum) + '-' + str(23 - seasonNum)
        season_select = Select(driver.find_element(By.CLASS_NAME, 'DropDown_select__4pIg9'))
        season_select.select_by_visible_text(season)
        time.sleep(2)
        pageDrop = Select(driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select'))
        pageDrop.select_by_visible_text("All")
        time.sleep(2)
        soup = load_soup_elment()
        rows = soup.find_all('tr')
        rows.pop(0)
        for row in rows:
            cells = row.find_all('td')
            rowNum = len(df)
            playerRow = []
            for index, value in enumerate(dictToDF.values()):
                if(index != 23):
                    playerRow.append(cells[index].text.strip())
                else:
                    playerRow.append(bioInfo(cells[1].find('a')['href']))
            df.loc[rowNum] = playerRow
        df.to_csv('Data.csv')

        driver.get(statsUrl)
    df.to_csv('Data.csv')
    driver.quit()
    
#getting_data()
get_all_star_data()
