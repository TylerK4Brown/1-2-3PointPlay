# Leaderboard page
# WIP - will display the current leaderboard for the year, with the ability to view previous years' leaderboards as well

import streamlit as st

st.title("Leaderboard for the current year", text_alignment="center")
st.markdown("Work in progress :smile:", text_alignment="center")
st.divider(width='stretch')

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")