# View picks page
# Calls the database to get the users picks
# Calls the Odds API to get live score updates for the picks by each user
import streamlit as st
from css.streamlit_css import load_css_gamedisplay
from API_info.odds_api_call import make_scores_api_call
from database_operations.database import update_user_points, get_all_user_picks
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import random

# over/under coverage math
def calculate_spread_cover(over_under_pick, over_under_score, score_home_team, score_away_team):
    primary_score = score_home_team + score_away_team if over_under_pick == "OVER" else over_under_score
    secondary_score = over_under_score if over_under_pick == "OVER" else score_home_team + score_away_team

    result = (primary_score - secondary_score)
    return result > 0

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
    print(f"MAKING API CALL FOR {name} | GAME ID LIST: {game_id_list}")
    pick_scores = make_scores_api_call(game_id_list)
    print(json.dumps(pick_scores, indent=2))
    iteration_index = 0
    
    for pick in sorted_picks:
        # Pull all relevant information from the output JSON object and store it in variables for easier access
        home_team = pick["home_team"]
        away_team = pick["away_team"]
        over_under = pick["over_under"]
        over_under_score = pick["over_under_score"]
        point_value = pick["point_value"]
        game_id = pick["game_id"]
        game_start = ""
        score_home_team = ""
        score_away_team = ""
        
        # iterate through each score returned by the API call to find the score for the current game ID
        for score in pick_scores:
            if score["id"] == game_id:
                game_start = score["commence_time"]
                if score["scores"] is None:
                    score_home_team = 0
                    score_away_team = 0
                else:
                    score_home_team = int(score["scores"][0]["score"])
                    score_away_team = int(score["scores"][1]["score"])
        
        # score_home_team = random.randint(0, 14)
        # score_away_team = random.randint(0, 14)
        # Convert game time from iso UTC format to Eastern Time and format it for display
        game_start = datetime.fromisoformat(game_start.replace("Z", "+00:00")).astimezone(ZoneInfo("America/New_York")).strftime("%A, %B %d, %Y at %I:%M %p")

        iteration_index += 1
        is_covering = calculate_spread_cover(over_under, over_under_score, score_home_team, score_away_team)
        current_week_total += (int(point_value)) if is_covering else 0
            
        # Build expander elements based on the information gathered above
        # Similar to the implementation in display_data.py, does not include the buttons
        col1, col2, col3 = st.columns([1, 5, 1])
        with col2:
            expander_string = f"{point_value} POINT PLAY: {away_team} @ {home_team} → → → → YOUR PICK: {over_under} {over_under_score} → → → → {'✅' if is_covering else '❌'}"
            with st.expander(expander_string, expanded=False):
                # create columns within the expander to display team logs
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.image(f"images_mlb/{away_team.lower()}.png", width=100, caption=f"{score_away_team}")
                    
                with col2:  
                    st.title(f"@", text_alignment='center') 
                with col3:
                    st.image(f"images_mlb/{home_team.lower()}.png", width=100, caption=f"{score_home_team}")
    
                st.markdown(f"## O/U: {over_under_score}", text_alignment='center')
                st.markdown(f"## YOUR PICK: {over_under} {over_under_score}", text_alignment='center')
                st.markdown(f"## **COVERING**: {'✅' if is_covering else '❌'}", text_alignment='center')
                st.markdown(f"## :red[GAME START: {game_start}]", text_alignment='center')
    
    # If there are no current totals for this week, update the database with the current week's total and add it to the accumulated points
    if row['current_week_total'] is None:
        # Display the points earned this week and the total amount of points accumulated so far
        # Print this first since it would sometimes bug out if the database updated before picks did
        st.markdown(f"### Points Today: {current_week_total}", text_alignment='center')
        st.markdown(f"### Total Points: {row['accumulated_points'] + current_week_total}", text_alignment='center')
        update_user_points(row["name"], current_week_total, current_week_total + row['accumulated_points'])
           
    # If the total for the current week has changed, find the difference, and update the accumulated points accordingly
    elif row['current_week_total'] != current_week_total:
        difference = current_week_total - row['current_week_total']
        # Display the points earned this week and the total amount of points accumulated so far
        # Print this first since it would sometimes bug out if the database updated before picks did
        st.markdown(f"### Points Today: {current_week_total}", text_alignment='center')
        st.markdown(f"### Total Points: {row['accumulated_points'] + difference}", text_alignment='center')
        update_user_points(row["name"], current_week_total, row['accumulated_points'] + difference)
    
    # If none of these conditions are met, still display the points earned and the total points for the week
    # No database updates are necessary since the current week's total has not changed
    else:
        st.markdown(f"### Points Today: {current_week_total}", text_alignment='center')
        st.markdown(f"### Total Points: {row['accumulated_points']}", text_alignment='center')
    
    st.divider(width='stretch')

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")