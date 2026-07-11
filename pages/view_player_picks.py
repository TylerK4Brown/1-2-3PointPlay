# View picks page
# Calls the database to get the users picks
# Calls the Odds API to get live score updates for the picks by each user

import streamlit as st
from st_supabase_connection import SupabaseConnection
from css.streamlit_css import load_css_gamedisplay
from API_info.odds_api_call import make_scores_api_call
from API_info.abbreviation_mapping import reverse_map_abbreviations
import random
import json

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

# Initialize database connection
conn = st.connection("user_picks", type=SupabaseConnection)
rows = conn.table("user_picks").select("*").execute().data
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
    st.divider(width='stretch')

    # Sort picks by point value, ascending order
    sorted_picks = sorted(row["current_picks"]["picks"], key=lambda pick: pick["point_value"])
    
    for pick in sorted_picks:
        # Pull all relevant information from the output JSON object and store it in variables for easier access
        abbreviation_mapping = reverse_map_abbreviations()
        home_team = pick["home_team"]
        away_team = pick["away_team"]
        point_spread = pick["spread"]
        point_value = pick["point_value"]
        is_pick_home = pick["is_pick_home"]
        spread_pick_abbreviation = point_spread.split(" ")[0] if len(point_spread.split(" ")) > 1 else None
        point_spread_pick = point_spread.split(" ")[1] if len(point_spread.split(" ")) > 1 else None
        score_home_team = ""
        score_away_team = ""
        pick_scores = make_scores_api_call(pick["game_id"])
        print(json.dumps(pick_scores, indent=2))
        
        # If there's no scores, don't list any
        # If there are, pull the scores from the JSON
        if pick_scores[0]["scores"] == None:
            score_home_team = 0
            score_away_team = 0
        else:
            score_home_team = pick_scores[0]["scores"][0]["score"]
            score_away_team = pick_scores[0]["scores"][1]["score"] 
        
        score_home_team = random.randint(0, 50)
        score_away_team = random.randint(0, 50)
        covering_spread = calculate_spread_cover(is_pick_home, point_spread, score_home_team, score_away_team)
        current_week_total += (int(point_value)) if covering_spread else 0
            
        # Build expander elements based on the information gathered above
        # Similar to the implementation in display_data.py, does not include the buttons
        col1, col2, col3 = st.columns([1, 5, 1])
        with col2:
            if point_spread_pick == None:
                expander_string = f"{point_value} POINT PLAY: {away_team} @ {home_team} → → → → YOUR PICK: EVEN → → → → Covering Spread: {'✅' if covering_spread else '❌'}"
            else:
                expander_string = f"{point_value} POINT PLAY: {away_team} @ {home_team} → → → → YOUR PICK: {spread_pick_abbreviation} {point_spread_pick} → → → → {'✅' if covering_spread else '❌'}"
            with st.expander(expander_string, expanded=False):
                # create columns within the expander to display team logs
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.image(f"images_nfl/{away_team.lower()}.png", width=100, caption=f"{score_away_team}")
                    
                with col2:  
                    st.title(f"@", text_alignment='center') 
                with col3:
                    st.image(f"images_nfl/{home_team.lower()}.png", width=100, caption=f"{score_home_team}")
                
                # display the spread information below the team logos
                if point_spread_pick == None:
                    st.markdown(f"## **SPREAD**: EVEN", text_alignment='center')
                else:
                    st.markdown(f"## **SPREAD**: {spread_pick_abbreviation} {point_spread_pick}", text_alignment='center')
               
                st.markdown("## YOUR PICK: " + point_spread, text_alignment='center')
                st.markdown(f"## **COVERING SPREAD**: {'✅' if covering_spread else '❌'}", text_alignment='center')
    
    # If there are no current totals for this week, update the database with the current week's total and add it to the accumulated points
    if row['current_week_total'] is None:
        # Display the points earned this week and the total amount of points accumulated so far
        # Print this first since it would sometimes bug out if the database updated before picks did
        st.markdown(f"### Points This Week: {current_week_total}", text_alignment='center')
        st.markdown(f"### Total Points: {row['accumulated_points'] + current_week_total}", text_alignment='center')
        conn.table("user_picks").update({
                "current_week_total": current_week_total, 
                "accumulated_points": current_week_total + row['accumulated_points']
            }).eq("name", row["name"]).execute()
       
        
    # If the total for the current week has changed, find the difference, and update the accumulated points accordingly
    elif row['current_week_total'] != current_week_total:
        difference = current_week_total - row['current_week_total']
        # Display the points earned this week and the total amount of points accumulated so far
        # Print this first since it would sometimes bug out if the database updated before picks did
        st.markdown(f"### Points This Week: {current_week_total}", text_alignment='center')
        st.markdown(f"### Total Points: {row['accumulated_points'] + difference}", text_alignment='center')
        conn.table("user_picks").update({
                "current_week_total": current_week_total, 
                "accumulated_points": row['accumulated_points'] + difference
            }).eq("name", row["name"]).execute()
        
    st.divider(width='stretch')

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")


    
    
    
    
    
    