# Landing page with three selector buttons
# The name selected will be stored in session state and used to personalize the picks page

import streamlit as st
from streamlit_extras.card_selector import *
from css.streamlit_css import load_css_buttons_homepage

st.title("Welcome to 1-2-3 Point Play!", text_alignment="center")
st.markdown("## Please select your name to continue to the picks page.", text_alignment="center")

if "name" not in st.session_state:
    st.session_state.name = ""
if "point_picks" not in st.session_state:
    st.session_state.point_picks = []

# Display three buttons for the user to select - clicking on a button will store the user's name in session state
# relocates to the make_your_picks page
load_css_buttons_homepage()
if st.button("Dad", width='stretch', key="dad_button"):
    st.session_state.name = "Dad"
    st.switch_page("pages/make_your_picks.py")

if st.button("TJ", width='stretch', key="tj_button"):
    st.session_state.name = "TJ"
    st.switch_page("pages/make_your_picks.py")

if st.button("Tyler", width='stretch', key="tyler_button"):
    st.session_state.name = "Tyler"
    st.switch_page("pages/make_your_picks.py")
