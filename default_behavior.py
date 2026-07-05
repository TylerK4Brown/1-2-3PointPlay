# Makes sure that on refresh, the user is redirected to the landing page to select a name
# On refresh, point_picks and name are no longer in the session state
# If one or the other is not present, redirect the user to the landing page to select a name and initialize the session states
import streamlit as st

def check_session_states():
    # Check if the session states for name and point_picks exist, if not, redirect to landing page
    if "name" not in st.session_state or "point_picks" not in st.session_state:
        st.title("NAME NOT SELECTED - PLEASE RETURN TO THE LANDING PAGE AND SELECT A NAME", text_alignment="center")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Return to Landing Page", width=700, key="return_landing_page"):
                st.switch_page("pages/landing_page.py")
        return False
    else:
        return True