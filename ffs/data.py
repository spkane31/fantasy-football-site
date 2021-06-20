from ffs.db import get_db
from typing import Dict, Tuple, List

from flask import Blueprint
from flask.templating import render_template

from ffs.db import get_db

bp = Blueprint("data", __name__)


# TODO: Let's change this to lowest 5, and add highest 5
def _find_alltime_low(data: Dict[str, str]) -> Tuple[float, str]:
    lowest = 200.0
    lowest_team = ""
    for year, week_dict in data.items():
        for week, matchups in week_dict.items():
            for m in matchups:
                if m["loser_score"] < lowest:
                    lowest = m["loser_score"]
                    lowest_team = m["loser"]

    return lowest, lowest_team


LOWEST_5 = "SELECT year, week, loser, loser_score FROM matchups ORDER BY loser_score ASC LIMIT 5"
HIGHEST_5 = "SELECT year, week, winner, winner_score FROM matchups WHERE year != 2017 and week != 14 ORDER BY winner_score DESC LIMIT 5"
BIGGEST_WINS = "SELECT id, (winner_score - loser_score) AS margin FROM matchups ORDER BY margin DESC LIMIT 5"
SELECT_QUERY = "SELECT year, week, winner, loser, winner_score, loser_score FROM matchups WHERE id = ?"


def matchups_to_json(data):
    ret = []
    for idx, d in enumerate(data):
        ret.append(
            {
                "rank": idx + 1,
                "year": d[0],
                "week": d[1],
                "team": d[2],
                "score": d[3],
            }
        )
    return ret


def full_matchup_to_json(data, idx):
    return {
        "rank": idx + 1,
        "year": data[0],
        "week": data[1],
        "winner": data[2],
        "loser": data[3],
        "winner_score": round(data[4], 2),
        "loser_score": round(data[5], 2),
        "difference": round(data[4] - data[5], 2),
    }


@bp.route("/")
def index():
    """Show all matchups"""
    db = get_db()
    cur = db.cursor()

    cur.execute(LOWEST_5)
    results = cur.fetchall()
    lows = matchups_to_json(results)

    cur.execute(HIGHEST_5)
    results = cur.fetchall()
    highs = matchups_to_json(results)

    cur.execute(BIGGEST_WINS)
    results = cur.fetchall()

    blowouts = []
    for idx, (id, difference) in enumerate(results):
        cur.execute(SELECT_QUERY, (id,))
        blowouts.append(full_matchup_to_json(cur.fetchone(), idx))

    return render_template("index.html", lows=lows, highs=highs, blowouts=blowouts)


@bp.route("/history")
def history():
    """Show all matchups"""
    return render_template("history.html", data={})


UNIQUE_TEAMS = "SELECT DISTINCT winner FROM matchups;"
WINS_COUNT = "SELECT COUNT(*) FROM matchups WHERE winner = ?"
LOSS_COUNT = "SELECT COUNT(*) FROM matchups WHERE loser = ?"
POINT_SCORED = "SELECT winner, loser, winner_score, loser_score FROM MATCHUPS"

def sort_by_key(data: List[Dict[str, str]], key: str) -> None:
    """Simple bubble sort on list of dicts based on one key"""
    for i in range(len(data)-1):
        for j in range(i, len(data)):
            if data[i][key] < data[j][key]:
                data[i], data[j] = data[j], data[i]


@bp.route("/all-time")
def all_time():
    """Show all time rankings"""
    data = []

    db = get_db()
    cur = db.cursor()

    result = cur.execute(UNIQUE_TEAMS)
    all_teams = result.fetchall()

    for team in all_teams:
        temp = {"team": team[0], "points": 0, "points_against": 0}

        cur.execute(WINS_COUNT, team)
        result = cur.fetchone()

        temp["wins"] = result[0]

        cur.execute(LOSS_COUNT, team)
        result = cur.fetchone()
        temp["losses"] = result[0]

        data.append(temp)

    sort_by_key(data, "wins")

    cur.execute(POINT_SCORED)
    for result in cur.fetchall():
        (winner, loser, winner_score, loser_score) = result
        for d in data:
            if d["team"] == winner:
                d["points"] += winner_score
                d["points_against"] += loser_score

            elif d["team"] == loser:
                d["points"] += loser_score
                d["points_against"] += winner_score

    # Get avg / game
    for d in data:
        d["points"] = round(d["points"], 2)
        d["points_against"] = round(d["points_against"], 2)
        d["points_per_game"] = round(d["points"] / (d["wins"] + d["losses"]), 2)
        d["points_against_per_game"] = round(d["points_against"] / (d["wins"] + d["losses"]), 2)

    return render_template("alltime.html", data=data)