import streamlit as st
from database_operations.database import get_picks_by_week

def get_pick_statistics(week_number, called_from):
    most_frequent_teams_picked = {}
    # if week number isn't a list, convert to a list so it can be iterated
    if not isinstance(week_number, list):
        week_number = [week_number]

    total_picks_covering = 0
    one_point_picks_covering = 0
    two_point_picks_covering = 0
    three_point_picks_covering = 0
    underdog_picks_covering, total_underdog_picks = 0, 0
    favorite_picks_covering, total_favorite_picks = 0, 0

    for week in week_number:
        if called_from == "overall":
            rows = get_picks_by_week(week, None)
        else:
            rows = get_picks_by_week(week, st.session_state.player_stats_selected)
        # 3 rows get returned, one for each user.
        # Each row contains a picks list for that week.
        # Iterate through each row and then through each pick list to count
        # the number of picks covering the spread.
        for row in rows:
            for picks in row[f"week_{week}"]["picks"]:
                spread = float(picks["spread_pick"].split(" ")[1])

                if picks["covering_spread"] == False or picks["covering_spread"] == "push":
                    if spread > 0:
                        total_underdog_picks +=1
                    elif spread < 0:
                        total_favorite_picks +=1

                elif picks["covering_spread"] == True:
                    total_picks_covering += 1
                    if spread > 0:
                        underdog_picks_covering += 1
                        total_underdog_picks += 1
                    elif spread < 0:
                        favorite_picks_covering += 1
                        total_favorite_picks += 1
                
                    if picks["point_value"] == "1":
                        one_point_picks_covering += 1
                    elif picks["point_value"] == "2":
                        two_point_picks_covering += 1
                    elif picks["point_value"] == "3":
                        three_point_picks_covering += 1
                
                team_picked = picks["spread_pick"].split(" ")[0]
                if team_picked not in most_frequent_teams_picked:
                    most_frequent_teams_picked[team_picked] = 0
                most_frequent_teams_picked[team_picked] += 1

    # return information in a dictionary to be used in the statistics page
    return {
        "total_picks_covering": total_picks_covering,
        "one_point_picks_covering": one_point_picks_covering,
        "two_point_picks_covering": two_point_picks_covering,
        "three_point_picks_covering": three_point_picks_covering,
        "underdog_picks_covering": underdog_picks_covering,
        "favorite_picks_covering": favorite_picks_covering,
        "total_underdog_picks": total_underdog_picks,
        "total_favorite_picks": total_favorite_picks,
        "most_frequent_teams_picked": most_frequent_teams_picked
    }