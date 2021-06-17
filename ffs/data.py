from typing import Dict, Tuple

import csv
import json

from flask import Blueprint, g
from flask.templating import render_template

bp = Blueprint("data", __name__)


# TODO: Let's change this to lowest 5, and add highest 5
def _find_alltime_low(data: Dict[str, str]) -> Tuple[float, str]:
    lowest = 200.0
    lowest_team = ""
    for year, week_dict in data.items():
        print(type(week_dict))
        for week, matchups in week_dict.items():
            print(type(matchups))
            print(matchups)
            for m in matchups:
                print(m)
                if m["loser_score"] < lowest:
                    lowest = m["loser_score"]
                    lowest_team = m["loser"]

    return lowest, lowest_team


@bp.route("/")
def index():
    """Show all matchups"""
    data = []
    with open("history.json") as f:
        data = json.load(f)

    low_score, low_team = _find_alltime_low(data)
    return render_template("index.html", data=data, lowest={"low_score": low_score, "low_team": low_team})
