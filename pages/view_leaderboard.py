## view_leaderboard.py
## Displays cumulative player standings using point and win/loss data fetched from the database
## Formats leaderboard output for quick comparison across all participants

import streamlit as st
from database_operations.database import get_user_points, get_win_loss_record
from display_helpers.number_formatting import format_points
from css.streamlit_css import load_css_gamedisplay

load_css_gamedisplay()
st.markdown("# Current leaderboard", text_alignment="center")
st.divider(width='stretch')

get_user_points()  # Call the function to retrieve and store user points in session state

leaderboard_dict = {
    "Dad": {
        "points": st.session_state.get("Dad_accumulated_points"),
        "win_loss_record": get_win_loss_record("Dad")
    },
    "TJ": {
        "points": st.session_state.get("TJ_accumulated_points"),
        "win_loss_record": get_win_loss_record("TJ")
    },
    "Tyler": {
        "points": st.session_state.get("Tyler_accumulated_points"),
        "win_loss_record": get_win_loss_record("Tyler")
    }
}

# Creates a tuple (name, data) for each item in the dictionary
# takes index 1 of that tuple (the data dictionary) to access points and win/loss record for sorting
# sorts the dictionary by that value
# returns a new dictionary with the sorted values
points_data_sorted = dict(sorted(leaderboard_dict.items(), 
                                 key=lambda item: (item[1]['points'], item[1]['win_loss_record']['picks_correct']), 
                                 reverse=True))

# enumerate makes it so we can get the index of the items stored in the dictionary
# this is paired with the medals in the list above
medals = ["🥇", "🥈", "🥉"]
for index, (name, data) in enumerate(points_data_sorted.items()):
    medal = f"{medals[index]}"
    points = data["points"]
    win_loss_record = data["win_loss_record"]
    points_string = "points" if points != 1 else "point"
    st.markdown(f"# {medal} {name}: {format_points(points)} {points_string}", text_alignment="center")
    if win_loss_record['picks_push'] == 0:
        st.markdown(f"### ({win_loss_record['picks_correct']} - {win_loss_record['picks_incorrect']})", text_alignment="center")
    else:
        st.markdown(f"### ({win_loss_record['picks_correct']} - {win_loss_record['picks_incorrect']} - {win_loss_record['picks_push']})", text_alignment="center")

st.divider(width='stretch')
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")