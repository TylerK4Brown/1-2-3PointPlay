# Picks page for the app
# Will eventually make an API call to The Odds API to gather MLB data and display it for the user to make their picks

import streamlit as st
import requests
from API_info.odds_api_call import make_api_call, display_data_mlb

if "name" not in st.session_state:
    st.title("NAME NOT SELECTED - PLEASE RETURN TO THE LANDING PAGE AND SELECT A NAME")

else:
    st.title(f"Welcome {st.session_state.name}!", text_alignment="center")
    # set a disabled state for the segmented controls buttons that are created in the display_data_mlb function.
    if "disabled" not in st.session_state:
        st.session_state.disabled = False
    make_api_call()
    
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    
    if st.button("Return to Landing Page", width=700):
        st.switch_page("pages/landing_page.py")

    # test editing the disabled state of the segmented controls buttons altogether
    if st.button("disable selections", width=700):
        st.session_state.disabled = True
        # rerun the page to reflect the disabled state
        st.rerun()