# Display user's picks on a new page when they click on the "View Your Picks" button on the picks page.
from time import sleep
from zoneinfo import ZoneInfo
from datetime import datetime
import streamlit as st
import json
from database_operations.database import create_user_db_entry, update_user_picks
from default_behavior import check_session_states
from css.streamlit_css import load_css_buttons_display_picks

if check_session_states():
    # Load custom CSS for display picks buttons
    load_css_buttons_display_picks()
    #iterate through the custom dictionary and display the user's picks
    st.title(f"Here are your picks, {st.session_state.name}!", text_alignment="center")
    st.markdown("#### Please carefully review your picks below.", text_alignment="center")
    st.markdown("#### If you are satisfied with your selections, click the 'FINALIZE PICKS' button at the bottom of the page to submit your picks.", text_alignment="center")
    st.divider(width='stretch')

    # Only display completed picks (point_value AND spread values must not be null)
    point_picks = [pick for pick in st.session_state.point_picks if pick["point_value"] is not None and pick["spread"] is not None]
    # Sort picks by point value in ascending order
    sorted_point_picks = sorted(point_picks, key=lambda pick: pick["point_value"])

    # If all picks are not complete (this list will be less than 3), disable the finalize button and display a warning message
    # Otherwise, enable the finalize button
    if len(point_picks) < 3:
        st.warning("WARNING: You have not completed all of your picks yet. If this is intentional, please proceed. Otherwise, complete all your picks before finalizing.", icon="‼️")
    
    print("UPDATED PICKS LISTING: ", json.dumps(sorted_point_picks, indent=2))

    # Loop over all picks and print them to the page
    for pick in sorted_point_picks:
        # put 20 in the middle to push the images on the right all the way to the right
        col1, col2, col3 = st.columns([1, 20, 1])
        with col2:
            st.image(f"images_nfl/{pick['away_team'].lower()}.png", width=75)
        with col2:
            st.markdown(f"### {pick['away_team']} @ {pick['home_team']}",)
            st.markdown(f"#### Your pick: {pick['spread']}", )
            st.markdown(f"#### Points: {pick['point_value']}", )
        with col2:
            st.image(f"images_nfl/{pick['home_team'].lower()}.png", width=75)
        
        st.divider(width='stretch')

    # buttons to finalize picks, continue making picks, or return to the landing page
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("FINALIZE PICKS", key="view_picks", type="primary", width="stretch"):
            # store the user's picks in the database
            time_of_submission = datetime.now((ZoneInfo("America/New_York"))).strftime("%A, %B %d, %Y at %I:%M %p")
            # Only store completed picks (point_value AND spread values must not be null)
            are_picks_finalized = False

            if len(point_picks) == 3:
                are_picks_finalized = True
            
            for pick in point_picks:
                pick["is_pick_in_database"] = True
                
            data = {
                "name": st.session_state.name,
                "time_of_submission": time_of_submission,
                "current_picks": {
                    "picks": point_picks
                },
                "are_picks_finalized": are_picks_finalized
            }
            # if an entry exists for the user, update it. If not, create a new entry
            try:
                create_user_db_entry(data)
            except Exception as e:
                update_user_picks(st.session_state.name, data)
                
            st.success("Your picks have been finalized! Navigating back to landing page...")
            sleep(2)
            st.switch_page("pages/landing_page.py")
                
    with col2:
        if "name" in st.session_state and "point_picks" in st.session_state:
            if st.button("Continue Making Picks", width=700, key="continue_making_picks"):
                st.switch_page("pages/make_your_picks.py")

    with col3:
        if st.button("Return to Landing Page", width=700, key="return_landing_page"):
            st.switch_page("pages/landing_page.py")
