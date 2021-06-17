import json
import os

from espn_api.football import League

SWID = os.environ["SWID"] 
ESPN_S2 = os.environ["ESPN_S2"] 

years = [2017, 2018, 2019, 2020]

PRINT_STR = "{}: {} \t{}: {}"

raw_data = {}

matchup_key = "{}-{}-{}-{}"

for year in years:
    league = League(league_id=345674, year=year, swid=SWID, espn_s2=ESPN_S2)

    for week in range(1, 15):

        for box_score in league.scoreboard(week):
            try:
                temp_key = matchup_key.format(
                    box_score.home_team.owner,
                    box_score.away_team.owner,
                    week,
                    year,
                )
                raw_data[temp_key] = {
                    "year": year,
                    "week": week,
                    "home_team": box_score.home_team.owner,
                    "away_team": box_score.away_team.owner,
                    "home_team_score": box_score.home_score,
                    "away_team_score": box_score.away_score
                }
                # raw_data
                # raw_data.append([
                #     year,
                #     week,
                #     box_score.home_team.owner,
                #     box_score.home_score,
                #     box_score.away_team.owner,
                #     box_score.away_score
                # ])
            except Exception as exc:
                print(year, week)
                print(exc)


with open('matchups.csv', mode='w') as f:
    json.dumps(raw_data, f, indent=4)

# import csv

# COLUMNS = ["Year", "Week", "HomeTeam", "HomeScore", "AwayTeam", "AwayScore"]

# with open('matchups.csv', mode='w') as f:
#     writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#     for d in raw_data:
#         writer.writerow(d)
