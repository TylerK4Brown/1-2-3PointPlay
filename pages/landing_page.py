# Landing page with three selector buttons
# The name selected will be stored in session state and used to personalize the picks page

import streamlit as st
from css.streamlit_css import load_css_buttons_homepage
from st_supabase_connection import SupabaseConnection

# Initialize database connection
conn = st.connection("user_picks", type=SupabaseConnection)

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

# Check the database for existing names, disable the buttons accordingly
rows = conn.table("user_picks").select("*").execute().data
for row_data in rows:
    if row_data["name"] == "Tyler":
        st.session_state.disable_tyler_button = True
        st.session_state.tyler_buttontext = f"Tyler (Picks submitted on {row_data['time_of_submission']})"
    elif row_data["name"] == "TJ":
        st.session_state.disable_tj_button = True
        st.session_state.tj_buttontext = f"TJ (Picks submitted on {row_data['time_of_submission']})"
    elif row_data["name"] == "Dad":
        st.session_state.disable_dad_button = True
        st.session_state.dad_buttontext = f"Dad (Picks submitted on {row_data['time_of_submission']})"

st.title("Welcome to 1-2-3 Point Play!", text_alignment="center")
st.markdown("## Please select your name to continue to the picks page.", text_alignment="center")
st.divider(width='stretch')

# Display three buttons for the user to select - clicking on a button will store the user's name in session state
# relocates to the make_your_picks page
load_css_buttons_homepage()
if st.button(st.session_state.dad_buttontext, width='stretch', key="dad_button", disabled=st.session_state.disable_dad_button):
    st.session_state.name = "Dad"
    st.switch_page("pages/make_your_picks.py")

if st.button(st.session_state.tj_buttontext, width='stretch', key="tj_button", disabled=st.session_state.disable_tj_button):
    st.session_state.name = "TJ"
    st.switch_page("pages/make_your_picks.py")

if st.button(st.session_state.tyler_buttontext, width='stretch', key="tyler_button", disabled=st.session_state.disable_tyler_button):
    st.session_state.name = "Tyler"
    st.switch_page("pages/make_your_picks.py")

# Leaderboard button to view the running leaderboard for the current year (and maybe previous years)
st.divider(width='stretch')

st.markdown("## View this week's picks!", text_alignment="center")
if st.button("View Leaderboard Information", width='stretch', key="view_player_picks"):
    st.switch_page("pages/view_player_picks.py")
