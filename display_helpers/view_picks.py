import streamlit as st

def display_player_picks(home_team, away_team, point_spread, point_value, spread_pick_abbreviation, point_spread_pick, score_home_team, score_away_team, covering_spread):
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

  