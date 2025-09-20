#scraping hoopshype.com to gather the current NBA contracts of all the NBA players in the league
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
options.add_argument("--headless")  # comment out for debugging - removes need to open up a browser window physically
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#initializing steps
url = 'https://hoopshype.com/salaries/players/'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
#response.content must only be gathering info in the moment of initial fire-up?

driver.get(url)
driver.execute_script("window.scrollTo(0, 1500);") #scroll page down so that button is shown
print("Scrolling through site...")
time.sleep(5) #give it time to scroll down (and for advertisements to pop in)
conn = sqlite3.connect('nba_salaries.db') #creates SQL database
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
            #gather the text from the rows and columns availble in the table
            ranking = cols[0].get_text(strip=True)
            player = cols[1].get_text(strip=True)
            twenty_five_salary = cols[2].get_text(strip=True).replace('$', '').replace(',', '')
            twenty_six_salary = cols[3].get_text(strip=True).replace('$', '').replace(',', '')
            twenty_seven_salary = cols[4].get_text(strip=True).replace('$', '').replace(',', '')
            twenty_eight_salary = cols[5].get_text(strip=True).replace('$', '').replace(',', '')
            print(f"Scrapping Player: {player}...") #debugging tool - actively show what data is being collected

            try:
                twenty_five_salary = int(twenty_five_salary)
            except:
                twenty_five_salary = None
            try:
                twenty_six_salary = int(twenty_six_salary)
            except:
                twenty_six_salary = None
            try:
                twenty_seven_salary = int(twenty_seven_salary)
            except:
                twenty_seven_salary = None
            try:
                twenty_eight_salary = int(twenty_eight_salary)
            except:
                twenty_eight_salary = None
            #start adding the data from the current page
            data.append((2025, ranking, player, twenty_five_salary))
            data.append((2026, ranking, player, twenty_six_salary))
            data.append((2027, ranking, player, twenty_seven_salary))
            data.append((2028, ranking, player, twenty_eight_salary))
    ##cursor.execute("DROP TABLE IF EXISTS player_salaries") #drop and clean out table if necessary
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_salaries (
        year INTEGER,
        ranking TEXT,
        player TEXT,
        salary INTEGER,
        UNIQUE(year, player)
    )
    ''')
    cursor.executemany('''
    INSERT OR IGNORE INTO player_salaries (year, ranking, player, salary) VALUES (?, ?, ?, ?)
    ''', data) #insert all the data into the database

    conn.commit()
page = 1
for _ in range(27):
    extract_data()
    try:
        #not a url change - need to click to the next page!
        next_btn = driver.find_element(By.XPATH, '//button[contains(@class, "hd3Vfp__hd3Vfp _3JhbLM__3JhbLM")]')
        next_btn.click()
        page += 1
        print(f"Clicking on to Page #{page}...")
        time.sleep(2)  #allow for new content to load
        soup = BeautifulSoup(driver.page_source, 'html.parser') #have to call BeautifulSoup again since new information has been populated
        
    except Exception as e: #thrown an exception when clicking doesn't work or ends
        print("Pagination ended or error occurred:", e)
        break

#Preview data using Pandas
df = pd.read_sql_query(
    "SELECT * FROM player_salaries", conn)
print(df) #print out the query to ensure the format is as intended
df.to_csv("nba_salaries.csv", index=False) #since free Tableau subscription doesn't allow for .db files to be opened, converting to a .csv file

conn.close()