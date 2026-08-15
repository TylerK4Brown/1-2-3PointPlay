## landing_page.py
## Houses buttons for all of the main functionality of our app
## First three buttons listed allows the user to select who they are, and stores it in session state
## Also provides access to viewing picks from this week/pick history, the leaderboard, and overall statistics

# Landing page with three selector buttons
# The name selected will be stored in session state and used to personalize the picks page

import streamlit as st
from css.streamlit_css import load_css_buttons_homepage
from database_operations.database import get_all_user_picks, get_user_picks

# Initialize button disabling sessions state variables - disables buttons if a name has already been logged in the database
if "disable_tyler_button" not in st.session_state and "tyler_buttontext" not in st.session_state:
    st.session_state.disable_tyler_button = False
    st.session_state.tyler_buttontext = "Tyler"

if "disable_tj_button" not in st.session_state and "tj_buttontext" not in st.session_state:
    st.session_state.disable_tj_button = False
    st.session_state.tj_buttontext = "TJ"

if "disable_dad_button" not in st.session_state and "dad_buttontext" not in st.session_state:
    st.session_state.disable_dad_button = False
    st.session_state.dad_buttontext = "Dad"

# Initialize session states for names and point picks, which will be used to track user selections and store them in the database at the end of the process
if "name" not in st.session_state:
    st.session_state.name = ""
if "point_picks" not in st.session_state:
    st.session_state.point_picks = []

# remove any DB picks from session state if they exist
# accomodates for the situation where a user selects the wrong name
if len(st.session_state.point_picks) != 0:
    st.session_state.point_picks = [existing_pick for existing_pick in st.session_state.point_picks if existing_pick["is_pick_in_database"] == False]

# Check the database for existing names, disable the buttons accordingly
rows = get_all_user_picks()
for row_data in rows:
    if row_data["name"] == "Tyler" and row_data["are_picks_finalized"]:
        st.session_state.disable_tyler_button = True
        st.session_state.tyler_buttontext = f"Tyler (Picks finalized on {row_data['time_of_submission']})"
    elif row_data["name"] == "TJ" and row_data["are_picks_finalized"]:
        st.session_state.disable_tj_button = True
        st.session_state.tj_buttontext = f"TJ (Picks finalized on {row_data['time_of_submission']})"
    elif row_data["name"] == "Dad" and row_data["are_picks_finalized"]:
        st.session_state.disable_dad_button = True
        st.session_state.dad_buttontext = f"Dad (Picks finalized on {row_data['time_of_submission']})"

st.title("Welcome to 1-2-3 Point Play!", text_alignment="center")
st.markdown("## Please select your name to continue to the picks page.", text_alignment="center")
st.divider(width='stretch')

# Display three buttons for the user to select - clicking on a button will store the user's name in session state
# relocates to the make_your_picks page
load_css_buttons_homepage()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(st.session_state.dad_buttontext, width='stretch', key="dad_button", disabled=st.session_state.disable_dad_button):
        st.session_state.name = "Dad"
        # load user picks from the database into session state if they exist
        # if they don't, user starts with an empty list of pick
        db_picks = get_user_picks(st.session_state.name)
        # defaults to none if no picks exist to ensure no error is thrown
        db_picks = db_picks[0]["current_picks"]["picks"] if db_picks[0]["current_picks"] is not None else None
        if db_picks is not None:
            st.session_state.point_picks = db_picks
        st.switch_page("pages/make_your_picks.py")

with col2:
    if st.button(st.session_state.tj_buttontext, width='stretch', key="tj_button", disabled=st.session_state.disable_tj_button):
        st.session_state.name = "TJ"
        # load user picks from the database into session state if they exist
        # if they don't, user starts with an empty list of picks
        db_picks = get_user_picks(st.session_state.name)
        # defaults to none if no picks exist to ensure no error is thrown
        db_picks = db_picks[0]["current_picks"]["picks"] if db_picks[0]["current_picks"] is not None else None
        if db_picks is not None:
            st.session_state.point_picks = db_picks
        st.switch_page("pages/make_your_picks.py")
        
with col3:
    if st.button(st.session_state.tyler_buttontext, width='stretch', key="tyler_button", disabled=st.session_state.disable_tyler_button):
        st.session_state.name = "Tyler"
        # load user picks from the database into session state if they exist
        # if they don't, user starts with an empty list of picks
        db_picks = get_user_picks(st.session_state.name)
        # defaults to none if no picks exist to ensure no error is thrown
        db_picks = db_picks[0]["current_picks"]["picks"] if db_picks[0]["current_picks"] is not None else None
        if db_picks is not None:
            st.session_state.point_picks = db_picks
        st.switch_page("pages/make_your_picks.py")

st.divider(width='stretch')

st.markdown("## Pick viewing options", text_alignment="center")
pickscol1, pickscol2, pickscol3, pickscol4 = st.columns([1, 2, 2, 1])
with pickscol2:
    if st.button("View Picks From This Week", width='stretch', key="view_player_picks"):
        st.switch_page("pages/view_player_picks.py")
with pickscol3:
    if st.button("View Picks History", width='stretch', key="view_pick_history"):
        st.switch_page("pages/view_pick_history.py")

st.divider(width='stretch')
st.markdown("## View the current leaderboard", text_alignment="center")
leaderboardcol1, leaderboardcol2, leaderboardcol3 = st.columns([1, 1, 1])
with leaderboardcol2:
    if st.button("View Leaderboard", width='stretch', key="view_leaderboard"):
        st.switch_page("pages/view_leaderboard.py")

st.divider(width='stretch')
st.markdown("## View overall statistics", text_alignment="center")
statscol1, statscol2, statscol3 = st.columns([1, 1, 1])
with statscol2:
    if st.button("View Statistics", width='stretch', key="view_statistics"):
        st.switch_page("pages/statistics.py")