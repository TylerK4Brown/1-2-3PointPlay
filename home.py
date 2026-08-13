## home.py
## Configures the Streamlit app shell and registers all navigation pages
## Serves as the application entrypoint

import streamlit as st

st.set_page_config(
    page_title="1-2-3 Point Play",
    page_icon="🗣️",
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
    ],
    "View Player Picks": [
        st.Page("pages/view_player_picks.py", title="View Player Picks"),
    ],
    "View Leaderboard": [
        st.Page("pages/view_leaderboard.py", title="View Leaderboard"),
    ],
    "View Statistics": [
        st.Page("pages/statistics.py", title="View Statistics"),
    ],
    "View Individual Player Statistics": [
        st.Page("pages/individual_statistics.py", title="View Individual Player Statistics"),
    ],
    "View Pick History": [
        st.Page("pages/view_pick_history.py", title="View Pick History"),
    ],
}

# Hide the navigation bar and run the app with the defined page structure
pg = st.navigation(pages, position="hidden")
pg.run()