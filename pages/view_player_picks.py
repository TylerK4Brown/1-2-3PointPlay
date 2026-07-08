# View picks page
# Calls the database to get the users picks
# Calls the Odds API to get live score updates for the picks by each user
import streamlit as st
from st_supabase_connection import SupabaseConnection
from css.streamlit_css import load_css_gamedisplay
from API_info.odds_api_call import make_scores_api_call
import json

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
    name = row["name"]
    st.markdown(f"## {name}", text_alignment="center")
    st.divider(width='stretch')

    # Sort picks by point value, ascending order
    sorted_picks = sorted(row["current_picks"]["picks"], key=lambda pick: pick["point_value"])
    
    for pick in sorted_picks:
        # Pull all relevant information from the output JSON object and store it in variables for easier access
        home_team = pick["home_team"]
        away_team = pick["away_team"]
        point_spread = pick["spread"]
        point_value = pick["point_value"]
        team_favored_abbreviation = point_spread.split(" ")[0] if len(point_spread.split(" ")) > 1 else None
        score_home_team = ""
        score_away_team = ""
        pick_scores = make_scores_api_call(pick["game_id"])
        print(json.dumps(pick_scores, indent=2))
        
        point_spread_favored = point_spread.split(" ")[1] if len(point_spread.split(" ")) > 1 else None
        
        # If there's no scores, don't list any
        # If there are, pull the scores from the JSON
        if pick_scores[0]["scores"] == None:
            score_home_team = "N/A"
            score_away_team = "N/A"
        else:
            score_home_team = pick_scores[0]["scores"][0]["score"]
            score_away_team = pick_scores[0]["scores"][1]["score"] 
            
        # Build expander elements based on the information gathered above
        # Similar to the implementation in display_data.py, does not include the buttons
        col1, col2, col3 = st.columns([1, 5, 1])
        with col2:
            if point_spread_favored == None:
                expander_string = f"{point_value} POINT PLAY:{away_team} @ {home_team} → → → → Spread: EVEN"
            else:
                expander_string = f"{point_value} POINT PLAY: {away_team} @ {home_team} → → → → Spread: {team_favored_abbreviation} {point_spread_favored}"
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
                if point_spread_favored == None:
                    st.markdown(f"## **SPREAD**: EVEN", text_alignment='center')
                else:
                    st.markdown(f"## **SPREAD**: {team_favored_abbreviation} {point_spread_favored}", text_alignment='center')
                    
    st.divider(width='stretch')

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")

   