# Landing page with three selector buttons
# The name selected will be stored in session state and used to personalize the picks page

import streamlit as st
from streamlit_extras.card_selector import *
from css.streamlit_css import load_css_buttons_homepage

st.title("Welcome to 1-2-3 Point Play!", text_alignment="center")
st.markdown("## Please select your name to continue to the picks page.", text_alignment="center")

if "name" not in st.session_state:
    st.session_state.name = ""

# Use columns to center the selector buttons
col1, col2, col3 = st.columns([1, 2, 1])

# card selector component from streamlit-extras
with col2:
    selected = card_selector(
        [
            dict(
                icon="💡",
                title="Tyler",
            ),
            dict(
                icon="👨",
                title="Dad",
            ),
            dict(
                icon="👦",
                title="TJ",
            ),
        ],
        key="card_selector",
    )

st.divider()

# switch to a page when a button is clicked
# also initializes the state that stores all user picks
# each button is tied to a list index
match selected:
    case 0:
        st.session_state.name = "Tyler"
        if "point_picks" not in st.session_state:
            st.session_state.point_picks = []
        st.switch_page("pages/make_your_picks.py")

    case 1:
        st.session_state.name = "Dad"
        if "point_picks" not in st.session_state:
            st.session_state.point_picks = []
        st.switch_page("pages/make_your_picks.py")

    case 2:
        st.session_state.name = "TJ"
        if "point_picks" not in st.session_state:
            st.session_state.point_picks = []
        st.switch_page("pages/make_your_picks.py")
