# Page configuration file for the app
# Starts with two pages, one for the landing page and one for making picks

import streamlit as st

st.set_page_config(
    page_title="1-2-3 Point Play",
    layout="wide"
)

pages = {
    "Welcome to 1-2-3 Point Play!": [
        st.Page("pages/landing_page.py", title="Landing Page", default=True),
    ],
    "Make Your Picks!": [
        st.Page("pages/make_your_picks.py", title="Make Your Picks"),
    ],
    "Display Your Picks": [
        st.Page("pages/display_picks.py", title="Display Your Picks"),
    ]
}

pg = st.navigation(pages, position="hidden")
pg.run()