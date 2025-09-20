import sqlite3
import pandas as pd
conn = sqlite3.connect('nba_salaries.db') #opening SQL database
#SQL query of joining table of player salaries with table of player PER metrics + additional metrics
df = pd.read_sql_query(
    "SELECT nba_player_per.player, player_salaries.year as salary_year, salary, per as per_24_25, games_played, mpg, true_shot, value_added, wins_added " \
    "FROM player_salaries "
    "JOIN nba_player_per " \
    "ON player_salaries.player = nba_player_per.player", conn)
print(df)
df.to_csv("nba_player_per_vs_salary.csv", index=False) #since free Tableau subscription doesn't allow for .db files to be opened, converting to a .csv file
conn.close()