
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
global url
url = "https://www.nba.com/stats/leaders"
html_stats_url = 'stats.html'

def load_soup_elment(html_name):
    html_file = open(html_name)
    soup = BeautifulSoup(html_file, 'html.parser')
    return soup

def bioInfo(playerUrl):
    driver.get(playerUrl)
    try:
        driver.find_element(By.LINK_TEXT, "Bio").click()
        print(driver.current_url)
        bio=driver.find_element(By.CLASS_NAME, "PlayerBio_player_bio__kIsc_").text
        print(bio)
    except :
        bio = "non"
    return bio

def getting_data():
    driver.get(url)
    ID, Name, Team, GP, Minute, Points, FGM, FGA, FG_P = ([] for i in range(9))
    Three_PM, Three_PA, Three_Per, FTM, FTA, FT_P = ([] for i in range(6))
    OREB, DREB, REB, AST, STL, BLK, TOV, EFF, BIO = ([] for i in range(9))
    soup = load_soup_elment(html_stats_url)
    rows = soup.find_all('tr')
    rows.pop(0)
    for row in rows:
        cells = row.find_all('td')
        ID.append(cells[0].text.strip())
        Name.append(cells[1].text.strip())
        Team.append(cells[2].text.strip())
        GP.append(cells[3].text.strip())
        Minute.append(cells[4].text.strip())
        Points.append(cells[5].text.strip())
        FGM.append(cells[6].text.strip())
        FGA.append(cells[7].text.strip())
        FG_P.append(cells[8].text.strip())
        Three_PM.append(cells[9].text.strip())
        Three_PA.append(cells[10].text.strip())
        Three_Per.append(cells[11].text.strip())
        FTM.append(cells[12].text.strip())
        FTA.append(cells[13].text.strip())
        FT_P.append(cells[14].text.strip())
        OREB.append(cells[15].text.strip())
        DREB.append(cells[16].text.strip())
        REB.append(cells[17].text.strip())
        AST.append(cells[18].text.strip())
        STL.append(cells[19].text.strip())
        BLK.append(cells[20].text.strip())
        TOV.append(cells[21].text.strip())
        EFF.append(cells[22].text.strip())
        BIO.append(bioInfo(cells[1].find('a')['href']))
        

    df = pd.DataFrame({'ID':ID, 'Name':Name, 'Team':Team, 'GP':GP, 'Minute':Minute,
    'Points':Points, 'FGM':FGM, 'FGA':FGA, 'FG_P':FG_P, '3PM':Three_PM, '3PA':Three_PA, '3P%':Three_Per,
    'FTM':FTM, 'FTA':FTA, 'FT%':FT_P, 'OREB':OREB, 'DREB':DREB, 'REB':REB, 'AST':AST, 'STL':STL, 'BLK':BLK, 'TOV':TOV, 'EFF':EFF, 'BIO':BIO})
    time.sleep(8)
    driver.quit()
    
getting_data()
