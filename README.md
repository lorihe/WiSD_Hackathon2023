## WiSD_Hackathon2023

### Introduction

This project was a submission to [Women in Sports Data](https://www.womeninsportsdata.org/) Hackathon2023, a six-week sprint program using NBA tracking data. The data was provided by [Sportradar](https://sportradar.com/?lang=en-us), containing "events" and "tracking" data from 18 NBA games, as well as information on participating players and teams.

 - Raw data
metadata: 1 json file. 18 rows containing general information about each game (team names, season, date, etc.)
metadata_player: 1 json file. 1533 rows containing information about players (name, height, date of birth, position, etc.)
metadata_teams: 1 json file. 56 rows containing information about teams (name, abbrev., etc.)
tracking: 18 jsonl files. Each file has 88,000-100,000 lines, containing frame-by-frame in-game information (player coordinate, ball coordinate, game clock, shot clock, etc.)
events: 18 jsonl files. Each file has 3500-3700 lines, containing event-by-event in-game information (event type, present players, game clock, shot clock, etc.)

This submission includes two parts: 
1. A shot success prediction model and players' shooting ability assessment based on the model;
2. A web application that a) visualizes tracking data to reveal each player's player pattern and b) displays player ability assessment results, for front office staff and coaches to review.

  - Screenshot of Web Application :
    
![Dashboard screenshot](https://github.com/lorihe/WiSD_Hackathon2023/blob/main/Dashboard%20Img%20Display.PNG?raw=true)

  - Interactive Display:
![Interactive Display](https://github.com/lorihe/WiSD_Hackathon2023/blob/main/Dashboard%20Interactive%20Display.gif?raw=true)


### Purpose & Motivation

The purpose of the project is to organize and visualize the comprehensive information within the provided dataset, in order to make it convenient for viewers to review facts about games and players.

### Solution 

I created an indicator ‘bX’, short for ‘beyond expectation’. As the shot success prediction model was built upon shot information of all shots made by all players, it reflects an overall shooting ability. Therefore, I use the model to predict each player’s previous shots. If a player scores while the model predicts ‘miss’ based on the scenario, the player performances beyond expectation and receives positive bX points, and vice versa. For the web application, I extract data with built pipelines and used plotly + Dash to visualize them on an interactive local web page, then display the bX scores calculated for all players in the data science part. Kde measurement is used to darken dots in areas where the player frequently moves to.

### How/When to Use Application/Recommendation

The application runs only when the linked datasets are available (For this project, the data is not available to the public). By reviewing and using the interactive tools of the application, front office staff and coach can check out: 1. Each player’s movement pattern in each quarter of each game; 2. Where on the court each player made shots in each game and which shots scored or missed; 3. A comparison between the selected player's bX scores on different shot types. 4. A comparison between bX scores of all players who attended the selected game.

If more datasets are provided in the same naming format and data structure, the project notebooks can be easily adjusted to include new data. 

### Difficulties and Challenges Faced During Process

a.) While switching the selection of games and players on the web application, it first took 10 seconds for the plot to show up, due to the large amount of information in the tracking data. After rewriting the pipeline to filter the jsonl file first instead of reading and transforming the whole file into dataframe, the loading time reduce to 5-8 seconds.
 b.) The total number of games provided is relatively small, thus the issue of quantity exists. For example, some players have more than 200 shots on record, while some only have 1 shot. In this project, players who have less than 10 shots on record were not considered for bX assessment. 
 c.) Basketball was not my specialized area, so I had to quickly study the basics of this sport. My mentors explained to me lots of detailed knowledge about basketball and help me a lot in tackling this challenge. 

### Next steps/ What would you like to add if given more time to work on your project?

The web application is not showing the game results yet. The next step is to retrieve that information and show the winner, the scores of both teams and ideally who scored on this web page.

Due to the timing and quantity of data, the bX assessment method was built in a relatively simple way. In the following steps, the method should be reviewed and adjusted to improve its justification. 

While separating ‘dribble shot’ and ‘non-dribble shot’, the method was to check event data and call an event ‘dribble shot’ if the row before it was noted as ‘dribble’ with the same player. This method should be reviewed and adjusted if needed.

___
**Dev environment:** <br />
[Requirement](https://github.com/lorihe/WiSD_Hackathon2023/blob/main/requirements.txt)

**Execute the dashboard application:** <br />
Run notebook '01_Data Processing', '03_Modeling and Assessment', '04_Dashboard', then open 'http://localhost:1020/' in web browser to view.

