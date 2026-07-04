# Picks page for the app
# Will eventually make an API call to The Odds API to gather MLB data and display it for the user to make their picks

import streamlit as st
from API_info.odds_api_call import make_api_call

if "name" not in st.session_state or "point_picks" not in st.session_state:
    st.title("NAME NOT SELECTED - PLEASE RETURN TO THE LANDING PAGE AND SELECT A NAME", text_alignment="center")

else:
    st.title(f"Welcome {st.session_state.name}!", text_alignment="center")
    # set a disabled state for the segmented controls buttons that are created in the display_data_mlb function.
    if "disabled" not in st.session_state:
        st.session_state.disabled = True
    make_api_call()

# TODO: submit button that will eventually reroute to a page that will require the user to confirm their picks
# will also contain checks to make sure all required values are filled out before allowing submission
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Submit Picks", width=700, key="submit_picks"):
        st.switch_page("pages/display_picks.py")

# centered return to landing page button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")