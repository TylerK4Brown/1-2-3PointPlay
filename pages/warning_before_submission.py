# Warning page before submission of picks
# Displays the user's name and ensures that the user is ready to submit before making the database call

import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from time import sleep
from default_behavior import check_session_states
from css.streamlit_css import load_css_buttons_display_picks
from database_operations.database import create_user_db_entry, update_user_picks

if check_session_states():
    load_css_buttons_display_picks()
    st.title(f"You are about to submit your picks on behalf of {st.session_state['name']}.", text_alignment="center")
    st.divider(width='stretch')
    
    # warning text
    st.markdown("#### If this is not your name, return to the landing page and select your name", text_alignment="center")
    st.markdown("#### Your current picks are saved, so selecting a new name will not reset those picks.", text_alignment="center")
    st.markdown("#### If you're still unsure about your picks, click on the \"No, return to View My Picks\" button below to review your picks before finalizing your submission.", text_alignment="center")
    st.divider(width='stretch')
    
    st.title(f"Are you sure you want to submit your picks, {st.session_state['name']}?", text_alignment="center")

    # Button columns
    # leftmost button returns to the display picks page
    # middle button stores picks in the database, returns to landing page
    # rightmost button returns to the landing page without storing picks in the database
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("No, return to View My Picks", key="return_to_picks", width="stretch"):
            st.switch_page("pages/display_picks.py")

    with col1:
        if st.button("Yes, submit my picks!", key="view_picks", type="primary", width="stretch"):
            # store the user's picks in the database
            time_of_submission = datetime.now((ZoneInfo("America/New_York"))).strftime("%A, %B %d, %Y at %I:%M %p")
            # Only store completed picks (point_value AND spread values must not be null)
            are_picks_finalized = False
            point_picks = [pick for pick in st.session_state.point_picks if pick["point_value"] is not None and pick["spread"] is not None]

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
    
    with col3:
        if st.button("Return to Landing Page", key="return_to_landing", width="stretch"):
            st.switch_page("pages/landing_page.py")