# View picks page
# Calls the database to get the users picks
# Calls the Odds API to get live score updates for the picks by each user
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from css.streamlit_css import load_css_gamedisplay
from services.odds_api_call import make_scores_api_call
from database_operations.database import update_user_points, get_all_user_picks, update_scores, get_week_number, update_win_loss_info, get_win_loss_by_week
from display_helpers.view_picks import display_player_picks
from display_helpers.number_formatting import format_points
import random

# spread coverage math
# sets the user's pick as the primary score, and the other team as the secondary score
# subtract the primary from the secondary, and then add the spread to the result (i.e. spread is -3.5, primary score is 40, secondary score is 37
# the result is (40 - 37) + (-3.5) = -0.5, which means the pick did not cover the spread)
def calculate_spread_cover(is_pick_home, point_spread, score_home_team, score_away_team):
    primary_score = score_home_team if is_pick_home else score_away_team
    secondary_score = score_away_team if is_pick_home else score_home_team

    if len(point_spread.split(" ")) > 1:
        result = (primary_score - secondary_score) + float(point_spread.split(" ")[1])
    else:
        result = (primary_score - secondary_score)

    if result > 0:
        return True
    if result < 0:
        return False
    if result == 0:
        return "push"

# database call to return every player's pick
rows = get_all_user_picks()

# Load css and sort the rows by the user's name
load_css_gamedisplay()
rows = sorted(rows, key=lambda user: user["name"])

st.title("This week's picks!", text_alignment="center")
st.divider(width='stretch')

# iterate through each users picks
for row in rows:
    current_week_total = 0
    correct_picks = 0
    push_picks = 0
    iteration_index = 0
    name = row["name"]
    st.markdown(f"## {name}", text_alignment="center")

    # If there's no picks for this user yet, continue to the next user in the loop
    if row["current_picks"] is None:
        st.markdown(f"#### {name} has no picks for this week yet.", text_alignment="center")
        st.divider(width='stretch')
        continue
    # Sort picks by point value, ascending order
    sorted_picks = sorted(row["current_picks"]["picks"], key=lambda pick: pick["point_value"])
    game_id_list = [pick["game_id"] for pick in sorted_picks]
    # Make an API call with all three game IDs for the current user's picks
    pick_scores = make_scores_api_call(game_id_list)
    
    for pick in sorted_picks:
        # Pull all relevant information from the output JSON object and store it in variables for easier access
        home_team = pick["home_team"]
        away_team = pick["away_team"]
        point_spread = pick["original_spread"]
        spread_pick = pick["spread_pick"]
        point_value = pick["point_value"]
        is_pick_home = pick["is_pick_home"]
        game_id = pick["game_id"]
        start_time = pick["start_time"]
        spread_pick_point_value = spread_pick.split(" ")[1] if spread_pick != "EVEN" else 0
        score_home_team = None
        score_away_team = None
        covering_spread = None

        # If a game has not started yet, set covering_spread to "not started"
        # This effectively skips all spread and score calculation, since none of it actually exists yet
        datetime_sample = "2026-08-20T23:00:01Z"
        # print(datetime.strptime(datetime_sample, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).strftime('%A, %B %d at %I:%M %p'))
        datetime_now = datetime.now().isoformat()
        if start_time > datetime_sample:
            covering_spread = "not started"
            score_home_team = 0
            score_away_team = 0
        # If the game has started, iterate through the scores returned by the API call to find the score for the current game ID
        # If the API call does not return a score for this game, use the scores stored in the database instead
        else:
            for score in pick_scores:
                if score["id"] == game_id:
                    if score["scores"] is None:
                        score_home_team = 0
                        score_away_team = 0
                    else:
                        score_home_team = int(score["scores"][0]["score"])
                        score_away_team = int(score["scores"][1]["score"])

            # If these scores are still empty, it means the API call did not return scores for this game
            # Use the scores stored in the database if this is the case
            if score_home_team == None and score_away_team == None:
                score_home_team = pick["home_team_score"]
                score_away_team = pick["away_team_score"]

            # score_home_team = random.randint(0, 50)
            # score_away_team = random.randint(0, 50)
            covering_spread = calculate_spread_cover(is_pick_home, spread_pick, score_home_team, score_away_team)
            if covering_spread == True:
                current_week_total += int(point_value)
                correct_picks += 1
            elif covering_spread == "push":
                current_week_total += int(point_value) / 2
                push_picks += 1

        display_player_picks(home_team, away_team, point_spread, point_value, spread_pick, score_home_team, score_away_team, covering_spread, start_time)

        # Update scores for this pick in the database
        # Combats the issue of API not allowing for the game score history to be pulled after x amount of days
        update_scores(row["name"], score_home_team, score_away_team, iteration_index, sorted_picks, covering_spread)
        iteration_index += 1

    # Get the current week number from the database to determine if this is the first week of the season or not
    # If it is the first week, there are no previous W/L records to pull, so the current week's W/L record will be used to update the database
    # Otherwise, use a previous week's W/L record to update the current week's W/L record in the database
    incorrect_picks = len(sorted_picks) - correct_picks - push_picks
    week_number = get_week_number()
    week_number -= 1
    if week_number >= 1:
        win_loss_data = get_win_loss_by_week(week_number, row["name"])
        correct_picks = correct_picks + win_loss_data['picks_correct']
        push_picks = push_picks + win_loss_data['picks_push']
        incorrect_picks = incorrect_picks + win_loss_data['picks_incorrect']
   
    # If there are no current totals for this week, update the database with the current week's total and add it to the accumulated points
    if row['current_week_total'] is None:
        # Display the points earned this week and the total amount of points accumulated so far
        # Print this first since it would sometimes bug out if the database updated before picks did
        st.markdown(f"### Points This Week: {format_points(current_week_total)}", text_alignment='center')
        st.markdown(f"### Total Points: {format_points(row['accumulated_points'] + current_week_total)}", text_alignment='center')
        update_user_points(row["name"], current_week_total, current_week_total + row['accumulated_points'])
        update_win_loss_info(row["name"], correct_picks, incorrect_picks, push_picks)
    
    # If the total for the current week has changed, find the difference, and update the accumulated points accordingly
    elif row['current_week_total'] != current_week_total:
        difference = current_week_total - row['current_week_total']
        # Display the points earned this week and the total amount of points accumulated so far
        # Print this first since it would sometimes bug out if the database updated before picks did
        st.markdown(f"### Points This Week: {format_points(current_week_total)}", text_alignment='center')
        st.markdown(f"### Total Points: {format_points(row['accumulated_points'] + difference)}", text_alignment='center')
        update_user_points(row["name"], current_week_total, row['accumulated_points'] + difference)
        update_win_loss_info(row["name"], correct_picks, incorrect_picks, push_picks)
    
    # If none of these conditions are met, still display the points earned and the total points for the week
    # No database update (except for a potential W/L change) is necessary since the current week's total has not changed
    else:
        st.markdown(f"### Points This Week: {format_points(current_week_total)}", text_alignment='center')
        st.markdown(f"### Total Points: {format_points(row['accumulated_points'])}", text_alignment='center')
        update_win_loss_info(row["name"], correct_picks, incorrect_picks, push_picks)
    
    st.divider(width='stretch')

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")