# View picks page
# Calls the database to get the users picks
# Calls the Odds API to get live score updates for the picks by each user
import streamlit as st
from css.streamlit_css import load_css_gamedisplay
from services.odds_api_call import make_scores_api_call
from database_operations.database import update_user_points, get_all_user_picks, update_scores, get_week_number, update_picks_correct
from display_helpers.view_picks import display_player_picks
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
    return result > 0

# database call to return every player's pick
rows = get_all_user_picks()

week_number = get_week_number()
# Load css and sort the rows by the user's name
load_css_gamedisplay()
rows = sorted(rows, key=lambda user: user["name"])

st.title("This week's picks!", text_alignment="center")
st.divider(width='stretch')

# iterate through each users picks
for row in rows:
    current_week_total = 0
    correct_picks = 0
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
        spread_pick_point_value = spread_pick.split(" ")[1] if spread_pick != "EVEN" else 0
        score_home_team = ""
        score_away_team = ""
        
        # iterate through each score returned by the API call to find the score for the current game ID
        for score in pick_scores:
            if score["id"] == game_id:
                if score["scores"] is None:
                    score_home_team = 0
                    score_away_team = 0
                    game_start = score["commence_time"]
                else:
                    score_home_team = int(score["scores"][0]["score"])
                    score_away_team = int(score["scores"][1]["score"])
                    game_start = score["commence_time"]
        
        # Calculate if the player is covering the spread using randomly generated test values
        score_home_team = random.randint(0, 50)
        score_away_team = random.randint(0, 50)
        covering_spread = calculate_spread_cover(is_pick_home, spread_pick, score_home_team, score_away_team)
        current_week_total += (int(point_value)) if covering_spread else 0
        correct_picks += 1 if covering_spread else 0

        display_player_picks(home_team, away_team, point_spread, point_value, spread_pick, score_home_team, score_away_team, covering_spread)

        # Update scores for this pick in the database
        # Combats the issue of API not allowing for the game score history to be pulled after x amount of days
        update_scores(row["name"], score_home_team, score_away_team, iteration_index, sorted_picks, covering_spread)
        iteration_index += 1

    win_loss_data = row["win_loss_record"]
    print(win_loss_data)
    incorrect_picks = len(sorted_picks) - correct_picks
    # If there are no current totals for this week, update the database with the current week's total and add it to the accumulated points
    if row['current_week_total'] is None:
        # Display the points earned this week and the total amount of points accumulated so far
        # Print this first since it would sometimes bug out if the database updated before picks did
        st.markdown(f"### Points This Week: {current_week_total}", text_alignment='center')
        st.markdown(f"### Total Points: {row['accumulated_points'] + current_week_total}", text_alignment='center')
        update_user_points(row["name"], current_week_total, current_week_total + row['accumulated_points'])
        update_picks_correct(row["name"], correct_picks + win_loss_data['picks_correct'], incorrect_picks + win_loss_data['picks_incorrect'])
    
    # If the total for the current week has changed, find the difference, and update the accumulated points accordingly
    elif row['current_week_total'] != current_week_total:
        difference = current_week_total - row['current_week_total']
        difference_correct_picks = correct_picks - win_loss_data['picks_correct']
        difference_incorrect_picks = incorrect_picks - win_loss_data['picks_incorrect']
        # Display the points earned this week and the total amount of points accumulated so far
        # Print this first since it would sometimes bug out if the database updated before picks did
        st.markdown(f"### Points This Week: {current_week_total}", text_alignment='center')
        st.markdown(f"### Total Points: {row['accumulated_points'] + difference}", text_alignment='center')
        update_user_points(row["name"], current_week_total, row['accumulated_points'] + difference)
        update_picks_correct(row["name"], win_loss_data['picks_correct'] + difference_correct_picks, win_loss_data['picks_incorrect'] + difference_incorrect_picks)
    
    # If none of these conditions are met, still display the points earned and the total points for the week
    # No database updates are necessary since the current week's total has not changed
    else:
        difference_correct_picks = correct_picks - win_loss_data['picks_correct']
        difference_incorrect_picks = incorrect_picks - win_loss_data['picks_incorrect']
        st.markdown(f"### Points This Week: {current_week_total}", text_alignment='center')
        st.markdown(f"### Total Points: {row['accumulated_points']}", text_alignment='center')
        update_picks_correct(row["name"], win_loss_data['picks_correct'] + difference_correct_picks, win_loss_data['picks_incorrect'] + difference_incorrect_picks)
    
    st.divider(width='stretch')

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")