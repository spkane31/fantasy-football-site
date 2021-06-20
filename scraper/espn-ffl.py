import argparse
import json
import os
import sqlite3

from dotenv import find_dotenv, load_dotenv
from espn_api.football import League, matchup

from ffs.db import get_db

load_dotenv(find_dotenv())

SWID = os.environ.get("SWID")
ESPN_S2 = os.environ.get("ESPN_S2")


def scrape_matchups():
    """Scrape all matchup data from 2017 to 2020"""
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
                        matchup_data[year][week].append(
                            {
                                "winner": box_score.home_team.owner.rstrip(" "),
                                "loser": box_score.away_team.owner.rstrip(" "),
                                "winner_score": box_score.home_score,
                                "loser_score": box_score.away_score,
                            }
                        )
                    else:
                        matchup_data[year][week].append(
                            {
                                "winner": box_score.away_team.owner.rstrip(" "),
                                "loser": box_score.home_team.owner.rstrip(" "),
                                "winner_score": box_score.away_score,
                                "loser_score": box_score.home_score,
                            }
                        )

                except Exception as exc:
                    print(year, week)
                    print(exc)

    with open("history.json", mode="w") as f:
        json.dump(matchup_data, f, indent=4)


def scrape_draft_data():
    """Scrape all draft data from 2017 to 2020"""
    draft_data = {}
    years = [2017, 2018, 2019, 2020]

    for year in years:
        draft_data[year] = {}
        league = League(league_id=345674, year=year, swid=SWID, espn_s2=ESPN_S2)

        count = 0
        print(f"Year: {year}")
        for pick in league.draft:
            draft_data[year][count] = {
                "Player": pick.playerName,
                "PlayerID": pick.playerId,
                "Round": pick.round_num,
                "RoundPick": pick.round_pick,
                "Team": pick.team.owner,
            }
            count += 1

    with open("drafts.json", mode="w") as f:
        json.dump(draft_data, f, indent=4)


def create_connection(db_file="instance/ffs.sqlite"):
    return sqlite3.connect(db_file)


INSERT_QUERY = "INSERT INTO matchups (year, week, winner, loser, winner_score, loser_score) VALUES (?, ?, ?, ?, ?, ?)"
TOTAL_QUERY = "SELECT COUNT(*) FROM matchups"


def get_count(table="matchups"):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(TOTAL_QUERY)
    result = cur.fetchone()
    conn.close()
    return result[0]


# TODO: This should do a check to make sure the entry is not already there.
def load_to_database():
    conn = create_connection()

    cur = conn.cursor()

    n = get_count()
    if n > 100:
        print(f"Count is {n}, not inserting more data")
        return

    with open("history.json") as f:
        data = json.load(f)

    for year, year_dict in data.items():
        for week, matchups in year_dict.items():
            for matchup in matchups:
                cur.execute(
                    INSERT_QUERY,
                    (
                        year,
                        week,
                        matchup["winner"],
                        matchup["loser"],
                        matchup["winner_score"],
                        matchup["loser_score"],
                    ),
                )

    cur.execute(TOTAL_QUERY)
    result = cur.fetchone()
    print(f"Inserted {result[0]} entries")

    conn.commit()
    conn.close()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scrape", help="Re-scrape all data from ESPN")
    parser.add_argument("--draft-only", help="Re-scrape all data from ESPN")
    parser.add_argument("--load", help="Load all data to database")
    args = parser.parse_args()

    if args.draft_only:
        scrape_draft_data()
    elif args.scrape:
        scrape_matchups()
    if args.load:
        load_to_database()
