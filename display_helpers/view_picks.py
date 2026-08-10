from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st

def display_player_picks(home_team, away_team, game_spread, point_value, spread_pick, score_home_team, score_away_team, covering_spread, start_time=None):
    # Build expander elements based on the information gathered above
    # Similar to the implementation in display_data.py, does not include the buttons
    col1, col2, col3 = st.columns([1, 5, 1])
    spread_emoji = "✅"
    if covering_spread == True:
        spread_emoji = "✅"
    elif covering_spread == False:
        spread_emoji = "❌"
    elif covering_spread == "push":
        spread_emoji = "➖"
    elif covering_spread == "not started":
        spread_emoji = "⏳"
    
    with col2:
        if spread_pick == "EVEN":
            expander_string = f"{point_value} POINT PLAY: {away_team} @ {home_team} → → → → YOUR PICK: EVEN → → → → Covering Spread: {spread_emoji}"
        else:
            expander_string = f"{point_value} POINT PLAY: {away_team} @ {home_team} → → → → YOUR PICK: {spread_pick} → → → → {spread_emoji}"
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
            if spread_pick == "EVEN":
                st.markdown(f"## **SPREAD**: EVEN", text_alignment='center')
            else:
                st.markdown(f"## **SPREAD**: {game_spread}", text_alignment='center')
            
            st.markdown(f"## YOUR PICK: {spread_pick}", text_alignment='center')
            if spread_emoji == "⏳":
                st.markdown(f"## **COVERING SPREAD**: {spread_emoji} (Game not started)", text_alignment='center')
            else:
                st.markdown(f"## **COVERING SPREAD**: {spread_emoji}", text_alignment='center')

            if start_time is not None:
                st.markdown(f"### :red[**GAME START TIME**: {datetime
                                                            .strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
                                                            .replace(tzinfo=ZoneInfo('UTC'))
                                                            .astimezone(ZoneInfo('America/New_York'))
                                                            .strftime('%A, %B %d at %I:%M %p')}]", text_alignment='center')

  