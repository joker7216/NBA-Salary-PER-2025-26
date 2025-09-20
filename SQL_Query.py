import sqlite3
import pandas as pd
conn = sqlite3.connect('nba_salaries.db') #creates SQL database
df = pd.read_sql_query(
    "SELECT player_salaries.year, player_salaries.player, player_salaries.salary, player_ratings.rating " \
    "FROM player_salaries " \
    "JOIN player_ratings " \
    "ON player_salaries.player = player_ratings.player AND player_salaries.year = player_ratings.year" \
    "", conn)
print(df)
df.to_csv("salaries_ratings.csv", index=False)
conn.close()
#check out the player names matching up - about 200 players are missing due to this mismatch

# df = pd.read_sql_query(
#     "SELECT *, " \
#     "AVG(salary) AS Average_Salary " \
#     "FROM player_salaries " \
#     "GROUP BY player " \
#     "ORDER BY AVG(salary) DESC", conn)


# df = pd.read_sql_query(
#     "SELECT *, " \
#     "SUM(COALESCE(twenty_five_salary, 0) + COALESCE(twenty_six_salary, 0) + COALESCE(twenty_seven_salary, 0) + COALESCE(twenty_eight_salary, 0)) / " \
#     "( " \
#     "CASE WHEN twenty_five_salary IS NOT NULL THEN 1 ELSE 0 END + " \
#     "CASE WHEN twenty_six_salary IS NOT NULL THEN 1 ELSE 0 END + " \
#     "CASE WHEN twenty_seven_salary IS NOT NULL THEN 1 ELSE 0 END + " \
#     "CASE WHEN twenty_eight_salary IS NOT NULL THEN 1 ELSE 0 END " \
#     ") AS average_contract_salary " \
#     "FROM player_salaries " \
#     "GROUP BY player", conn)