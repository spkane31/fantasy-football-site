from ffs.db import get_db
from typing import Dict, Tuple

import csv
import json

from flask import Blueprint, g
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
        ret.append({
            "rank": idx + 1,
            "year": d[0],
            "week": d[1],
            "team": d[2],
            "score": d[3],
        })
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