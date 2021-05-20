from espn_api.football import League

SWID = "cf3eab51-0829-4ff2-a81d-2dea916b595c"
ESPN_S2 = "AECK7%2FdSy110uy1LJjLNEWviSqZafaghXHVFzw4R%2BIOcN9%2FhOojApRtqG%2FvTTFiG61YTFYD5DEOLWPHYyEk%2FyrT0yARf%2FvP7fdbOkSJOCVXWJvVTsUNeOvzCS34v7UDlZ7NwrmfzhEdwqt7W1%2BrmUnbVRH%2Blz20Q6FmRdN3372i08v96ip4MzQQkep%2FU0J0G5mxB1ASmh8ZdfmMbe%2BxwD0Bs6kEViVHD4m71MniuWh0eCkDdH%2BQIUqKuucgSiPDszdPissjj1GBnrlmM6K9gOf3w"

years = [2017, 2018, 2019, 2020]

PRINT_STR = "{}: {} \t{}: {}"

raw_data = []

for year in years:
    league = League(league_id=345674, year=year, swid=SWID  , espn_s2=ESPN_S2)

    for week in range(1, 15):

        for box_score in league.scoreboard(week):
            try:
                raw_data.append([
                    year,
                    week,
                    box_score.home_team.owner,
                    box_score.home_score,
                    box_score.away_team.owner,
                    box_score.away_score
                ])
            except Exception as exc:
                print(year, week)
                print(exc)
            # print(PRINT_STR.format(
            #     box_score.home_team.owner,
            #     box_score.home_score,
            #     box_score.away_team.owner,
            #     box_score.away_score
            # ))
    #     break
    # break

import csv

COLUMNS = ["Year", "Week", "HomeTeam", "HomeScore", "AwayTeam", "AwayScore"]

with open('matchups.csv', mode='w') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for d in raw_data:
        writer.writerow(d)
