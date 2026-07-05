from pandas import col
import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import datetime
from zoneinfo import ZoneInfo
from time import sleep

if "name" not in st.session_state or "point_picks" not in st.session_state:
    st.title("NAME NOT SELECTED - PLEASE RETURN TO THE LANDING PAGE AND SELECT A NAME", text_alignment="center")
else:
    conn = st.connection("user_picks", type=SupabaseConnection)
    st.title(f"You are about to submit your picks on behalf of {st.session_state['name']}.", text_alignment="center")
    st.divider(width='stretch')

    st.markdown("#### If this is not your name, return to the landing page and select your name", text_alignment="center")
    st.markdown("#### Your current picks are saved, so selecting a new name will not reset those picks.", text_alignment="center")
    st.markdown("#### If you're still unsure about your picks, click on the \"No, return to View My Picks\" button below to review your picks before finalizing your submission.", text_alignment="center")
    st.divider(width='stretch')

    st.title(f"Are you sure you want to submit your picks, {st.session_state['name']}?", text_alignment="center")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("No, return to View My Picks", key="return_to_picks", width="stretch"):
            st.switch_page("pages/display_picks.py")

    with col2:
        if st.button("Yes, submit my picks!", key="view_picks", type="primary", width="stretch"):
            # store the user's picks in the database
            time_of_submission = datetime.now((ZoneInfo("America/New_York"))).strftime("%A, %B %d, %Y at %I:%M %p")
            # Only store completed picks (point_value AND over_under values must not be null)
            point_picks = [pick for pick in st.session_state.point_picks if pick["point_value"] is not None and pick["over_under"] is not None]

            data = {
                "name": st.session_state.name,
                "time_of_submission": time_of_submission,
                "current_picks": {
                    "picks": point_picks
                }
            }
            # execute the insert query, store data in database
            conn.table("user_picks").insert(data).execute()
            st.success("Your picks have been finalized! Navigating back to landing page...")
            sleep(2)
            st.switch_page("pages/landing_page.py")
    
    with col3:
        if st.button("No, return to landing page.", key="return_to_landing", width="stretch"):
            st.switch_page("pages/landing_page.py")