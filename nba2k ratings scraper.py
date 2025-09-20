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
options.add_argument("--headless")  # comment out for debugging - removes need to open up a browser window
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#gather initial steps
url = 'https://www.hoopshype.com/nba-2k/players/?game=nba-2k25' #keeping it to 2K25 for the time being as the latest data
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
#response.content must only be gathering info in the moment of initial fire-up?

driver.get(url)
driver.execute_script("window.scrollTo(0, 1500);") #scroll page down so that button is shown
print("Scrolling through site...")
time.sleep(5) #give it time to scroll down (and for advertisements to pop in)
conn = sqlite3.connect('nba_salaries.db') #creates SQL database if not created already
cursor = conn.cursor() #used to execute SQL queries and output results

def extract_data(): #function that parses data and adds to the SQL database 
    # Grab rows from the salary table
    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # Skip header
    print(f"Scraping {len(rows)} rows...")

    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 3:
            #ranking = cols[0].get_text(strip=True)
            player = cols[1].get_text(strip=True)
            rating = cols[2].get_text(strip=True)
            print(f"Scrapping Player: {player}...")
            try:
                rating = int(rating)
            except:
                rating = None
            data.append((2025, player, rating))
            # data.append((2026, ranking, player, twenty_six_salary))
            # data.append((2027, ranking, player, twenty_seven_salary))
            # data.append((2028, ranking, player, twenty_eight_salary))
    #cursor.execute("DROP TABLE IF EXISTS player_salaries") #drop and clean out table if necessary
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_ratings (
        year INTEGER,
        player TEXT,
        rating INTEGER,
        UNIQUE(year, player)
    )
    ''')
    cursor.executemany('''
    INSERT OR IGNORE INTO player_ratings (year, player, rating) VALUES (?, ?, ?)
    ''', data)

    conn.commit()
page = 1
for _ in range(24):
    extract_data()
    try:
        #next_btn = driver.find_element(By.CLASS_NAME, "button.hd3Vfp__hd3Vfp._3JhbLM__3JhbLM")
        #clicking on to the next page!
        next_btn = driver.find_element(By.XPATH, '//button[contains(@class, "hd3Vfp__hd3Vfp _3JhbLM__3JhbLM")]')
        next_btn.click()
        page += 1
        print(f"Clicking on to Page #{page}...")
        time.sleep(2)  # Wait for new content
        soup = BeautifulSoup(driver.page_source, 'html.parser') #this goes ahead and grabs the new snapshot of the screen
        
    except Exception as e:
        print("Pagination ended or error occurred:", e)
        break

# Step 3 (optional): Preview data using Pandas
df = pd.read_sql_query(
    "SELECT * FROM player_ratings", conn)
print(df)
df.to_csv("2k_ratings.csv", index=False)
conn.close()