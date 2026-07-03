# Picks page for the app
# Will eventually make an API call to The Odds API to gather MLB data and display it for the user to make their picks

import streamlit as st
import requests

if "name" not in st.session_state:
    st.title("NAME NOT SELECTED - PLEASE RETURN TO THE LANDING PAGE AND SELECT A NAME")

else:
    st.title(f"Welcome {st.session_state.name}!", text_alignment="center")
    st.markdown("## Please make your picks for the upcoming WNBA games below.", text_alignment="center")

    
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700):
        st.switch_page("pages/landing_page.py")