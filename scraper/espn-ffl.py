import json
import os

from dotenv import find_dotenv, load_dotenv
from espn_api.football import League, matchup

load_dotenv(find_dotenv())

SWID = os.environ["SWID"] 
ESPN_S2 = os.environ["ESPN_S2"] 

matchup_data = {}
years = [2017, 2018, 2019, 2020]

PRINT_STR = "{}: {}"

for year in years:
    matchup_data[year] = {}
    league = League(league_id=345674, year=year, swid=SWID, espn_s2=ESPN_S2)

    for week in range(1, 15):
        matchup_data[year][week] = []
        print(PRINT_STR.format(year, week))
        for box_score in league.scoreboard(week):
            try:
                if box_score.home_score > box_score.away_score:
                    matchup_data[year][week].append({
                        "winner": box_score.home_team.owner.rstrip(" "),
                        "loser": box_score.away_team.owner.rstrip(" "),
                        "winner_score": box_score.home_score,
                        "loser_score": box_score.away_score,
                    })
                else:
                    matchup_data[year][week].append({
                        "winner": box_score.away_team.owner.rstrip(" "),
                        "loser": box_score.home_team.owner.rstrip(" "),
                        "winner_score": box_score.away_score,
                        "loser_score": box_score.home_score,
                    })

            except Exception as exc:
                print(year, week)
                print(exc)


with open('history.json', mode='w') as f:
    json.dump(matchup_data, f, indent=4)
