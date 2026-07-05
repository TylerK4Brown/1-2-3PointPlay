# Display user's picks on a new page when they click on the "View Your Picks" button on the picks page.
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from st_supabase_connection import SupabaseConnection
import json
from time import sleep

# if these are not in the session state, redirect the user back to the landing page
# selecting a name in the landing page will initialize these session states
if "name" not in st.session_state or "point_picks" not in st.session_state:
    st.title("NAME NOT SELECTED - PLEASE RETURN TO THE LANDING PAGE AND SELECT A NAME", text_alignment="center")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Return to Landing Page", key="return_to_landing", width="stretch"):
            st.switch_page("pages/landing_page.py")

# otherwise, iterate through the custom dictionary and display the user's picks
else:
    st.title(f"Here are your picks, {st.session_state.name}!", text_alignment="center")
    st.markdown("#### Please carefully review your picks below.", text_alignment="center")
    st.markdown("#### If you are satisfied with your selections, click the 'FINALIZE PICKS' button at the bottom of the page to submit your picks.", text_alignment="center")
    st.divider(width='stretch')

    # Only display completed picks (point_value AND over_under values must not be null)
    point_picks = [pick for pick in st.session_state.point_picks if pick["point_value"] is not None and pick["over_under"] is not None]
    # Sort picks by point value in ascending order
    sorted_point_picks = sorted(point_picks, key=lambda pick: pick["point_value"])

    # If all picks are not complete (this list will be less than 3), disable the finalize button and display a warning message
    # Otherwise, enable the finalize button
    if len(point_picks) < 3:
        st.warning("You have not completed all of your picks yet. The 'FINALIZE PICKS' button will be enabled once all picks are completed.", icon="‼️")
        st.session_state.disabled = True
    else:
        st.session_state.disabled = False
    
    print("UPDATED PICKS LISTING: ", json.dumps(sorted_point_picks, indent=2))

    # Loop over all picks and print them to the page
    for pick in sorted_point_picks:
        # put 20 in the middle to push the images on the right all the way to the right
        col1, col2, col3 = st.columns([1, 20, 1])
        with col1:
            st.image(f"images/{pick['away_team'].lower()}.png", width="stretch")
        with col2:
            st.markdown(f"### {pick['away_team']} @ {pick['home_team']}", text_alignment="center")
            st.markdown(f"#### Your pick: {pick['over_under']} (O/U: {pick['over_under_score']})", text_alignment="center")
            st.markdown(f"#### Points: {pick['point_value']}", text_alignment="center")
        with col3:
            st.image(f"images/{pick['home_team'].lower()}.png", width="stretch")
        
        st.divider(width='stretch')

    # buttons to finalize picks, continue making picks, or return to the landing page
    col1, col2, col3 = st.columns([1, 1, 1])
    # TODO: Make this call a function that will call upon a database to store the user's picks and their name, and then return to the landing page
    if "disabled" in st.session_state:
        with col2:
            if st.button("FINALIZE PICKS", width=700, key="finalize_picks", type="primary", disabled=st.session_state.disabled):
                st.switch_page("pages/warning_before_submission.py")
                
    with col1:
        if "name" in st.session_state and "point_picks" in st.session_state:
            if st.button("Continue Making Picks", width=700, key="continue_making_picks"):
                st.switch_page("pages/make_your_picks.py")

    with col3:
        if st.button("Return to Landing Page", width=700, key="return_landing_page"):
            st.switch_page("pages/landing_page.py")
