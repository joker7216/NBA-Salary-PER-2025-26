#scraping espn.com to gather the PER metrics calculated for NBA players that qualify
import requests
from bs4 import BeautifulSoup #allows parsing of HTML and XML
import sqlite3
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
#options.add_argument("--headless")  # comment out for debugging - removes need to open up a browser window
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
def extract_data(): #function that parses data and adds to the SQL database 
    # Grab rows from the salary table
    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # Skip header
    print(f"Scraping {len(rows)} rows...")

    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 3:
            player = cols[1].get_text(strip=True).split(",")[0]
            games_played = cols[2].get_text(strip=True)
            mpg = cols[3].get_text(strip=True)
            true_shot = cols[4].get_text(strip=True)
            per = cols[11].get_text(strip=True)
            value_added = cols[12].get_text(strip=True)
            wins_added = cols[13].get_text(strip=True)
            print(f"Scrapping Player: {player}...")

            data.append((2024, player, games_played, mpg, true_shot, per, value_added, wins_added))
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nba_player_per (
        year INTEGER,
        player TEXT,
        games_played INTEGER,
        mpg DECIMAL, 
        true_shot DECIMAL, 
        per DECIMAL, 
        value_added DECIMAL, 
        wins_added DECIMAL,
        UNIQUE(year, player)
    )
    ''')
    cursor.executemany('''
    INSERT OR IGNORE INTO nba_player_per (year, player, games_played, mpg, true_shot, per, value_added, wins_added) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)


#gather initial steps
base_url = 'http://insider.espn.com/nba/hollinger/statistics' #need to find the right website
num_pages = 8

for page in range(1, num_pages + 1):
    if page == 1:
        url = base_url
    else:
        url = f"{base_url}/_/page/{page}" #each page has its separate URL, so will simply need a change in value in URL

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser') #gathering new information as each page comes up

    driver.get(url)
    driver.execute_script("window.scrollTo(0, 1000);") #scroll page down so that button is showing
    print("Scrolling through site...")
    time.sleep(2) #give it time to scroll down (and for advertisements to pop in)
    conn = sqlite3.connect('nba_salaries.db') #creates/opens SQL database
    cursor = conn.cursor() #used to execute SQL queries and output results
    extract_data()
    conn.commit() #committing changes
#cursor.execute("DROP TABLE IF EXISTS nba_player_per") #drop and clean out table if necessary

#Preview data using Pandas
df = pd.read_sql_query(
    "SELECT * FROM nba_player_per", conn)
print(df)
df.to_csv("nba_player_per.csv", index=False) #since free Tableau subscription doesn't allow for .db files to be opened, converting to a .csv file
conn.close() #closing connection to database