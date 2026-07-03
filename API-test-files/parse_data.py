# Example parsing script for the Odds API
# Gathers home team and away team name, as well as the point spread
# Also displays the bookmaker that provided said information

import json

def display_data (data, spread, team_name):
    print("---- LISTING OF UPCOMING GAMES AND THEIR POINT SPREADS ----")

    for data_obj in data:
        print(f"Home Team: {data_obj['home_team']}")
        print(f"Away Team: {data_obj['away_team']}")
        for spreads in data_obj["bookmakers"][0]["markets"][0]["outcomes"]:
            if spreads["point"] < 0:
                team_name = spreads["name"]
                spread = spreads["point"]
                book = data_obj["bookmakers"][0]["title"]
                break
            
        print(f"Spread favors {team_name}, {spread}. Information from {book} \n")