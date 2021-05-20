import csv

from flask import Blueprint, g
from flask.templating import render_template

bp = Blueprint("data", __name__)


@bp.route("/")
def index():
    """Show all matchups"""
    data = []
    with open("matchups.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            data.append({
                "Year": row[0],
                "Week": row[1],
                "Home": row[2],
                "HomeScore": row[3],
                "Away": row[4],
                "AwayScore": row[5],
            })
    return render_template("index.html", matchups=data)
