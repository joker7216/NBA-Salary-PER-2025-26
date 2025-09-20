# NBA Salary vs Player Efficiency Analysis (2025-26)

## Project Overview

This analysis examines the relationship between Player Efficiency Rating (PER) and player salaries. By comparing past performance with future compensation, we explore whether players are “earning” their wages and if teams are fairly valuing talent. Results are directional, not definitive. PER favors offensive contributions and may underrepresent defensive impact, so insights should be interpreted as indicators rather than absolute truths.

Horizontal and vertical lines mark the average PER and salary, with their intersection representing the baseline player.
The trend line shows the link between efficiency and pay, with confidence bands marking the ‘fair value’ range.
Players above the trend line (blue) are delivering greater value relative to salary, while players below (red) appear overvalued. This "Efficiency Residual" is explored with the top and bottom players relative to their salary.

## Table of Contents

- [Project Features](#project-features)
- [Methodology](#methodology)
- [How to Use](#how-to-use)
- [Results & Insights](#results--insights)
- [Future Work](#future-work)
- [References](#references)
- [Author](#author)
- [Glossary](#glossary)

Data was collected, cleaned, and merged to align salary and performance metrics.

## Project Features

- Interactive Tableau dashboard showcasing salary vs. PER
- Linear regression trend lines to highlight efficiency
- Residual analysis to identify over- and under-performing players
- Glossary included for terms and metrics

## Methodology

Data was collected from HoopsHype.com (player salaries) and ESPN.com (player performance statistics) via web scraping, targeting the relevant tables for each player. The workflow included the following steps:

Web Scraping
Tables containing player salaries and performance metrics were extracted using Python scripts. HTML tables were parsed and cleaned to ensure consistent formatting, handling missing values and converting numeric strings to appropriate data types as necessary.

Database Storage
Scraped data was stored in SQLite databases, with separate tables for salaries and performance metrics. Relationships were established in SQLite to align each player’s salary with their corresponding performance metrics using unique player identifiers (i.e. the player's name).

Querying and Merging
SQL queries were used to merge salary and performance tables, ensuring all metrics were correctly linked to the respective players. This included joining on player names and verifying consistency across datasets to avoid mismatches.

Export for Tableau
Since the free version of Tableau Public does not allow direct .db (SQLite) file connections, the final merged tables were exported as .csv files. These .csv files then served as the data sources for the interactive Tableau dashboards.

## How to Use

View the Tableau Public dashboard here: (https://public.tableau.com/views/Bucksvs_BoardsNBA2025-26Edition/NBASalaryvs_PlayerEfficiency?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
Use filters to explore players. Hover over points to see player's PER and salary relationship, as well as a simple assessment of whether or not the player is above/below the linear regression line.

## Results & Insights

[2025-26 Salary Vs. 2024-25 PER Rating](images/SalariesPERPlayersGraph.png)
We were able to identify top value players exceeding expectations relative to their salary. It also highlighted players whose salaries may not align with on-court performance. The reader should always remember that this is only one single relationship that is explored in this - one of hundreds, if not thousands of types of analyses that are done to determine if player's are worth their merit. However, these types of insights can inform management decisions and analytics-driven evaluations.

[Top 10 & Bottom 10 Players by Efficiency Residuals](images/TopBottomResidualsGraph.png)

## Future Work

- Expand analysis to multi-year salary trends
- Incorporate additional advanced metrics like Win Shares/48, VORP
- Integrate predictive modeling for expected future performance

## Glossary

PER: Player Efficiency Rating, the overall rating of a player's per-minute statistical production.
Residual: Actual PER - Predicted PER (Salary Linear Regression). This means more/less efficiency value.
Players on pace to play 500 or more minutes
To qualify: a player must have played 6.09 MPG.

Created by John Hollinger, PER can be recreated through formulas that includes positive accomplishments such as field goals, free throws, 3-pointers, assists, rebounds, blocks and steals, and negative ones such as missed shots, turnovers and personal fouls.

Two important things to remember about PER are that it's per-minute and is pace-adjusted.

## References

- HoopsHype: https://hoopshype.com
- ESPN Stats: http://insider.espn.com/nba/hollinger/statistics

## Author

Kevin Rocha
[LinkedIn](https://www.linkedin.com/in/kevinjrocha) – kevinrocha7216@gmail.com

Check out my Tableau profile: https://public.tableau.com/app/profile/kevin.rocha6997/vizzes
