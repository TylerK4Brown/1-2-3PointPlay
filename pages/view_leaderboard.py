import streamlit as st
from database_operations.database import get_user_points
from css.streamlit_css import load_css_gamedisplay

load_css_gamedisplay()
st.markdown("# Current leaderboard", text_alignment="center")
st.divider(width='stretch')

get_user_points()  # Call the function to retrieve and store user points in session state

points_data = {
    "Dad": st.session_state.get("Dad_accumulated_points"),
    "TJ": st.session_state.get("TJ_accumulated_points"),
    "Tyler": st.session_state.get("Tyler_accumulated_points")
}

# Creates a tuple, takes index 1 (points value) from the tuple for each item in the dictionary
# sorts the dictionary by that value
# returns a new dictionary with the sorted values
points_data_sorted = dict(sorted(points_data.items(), key=lambda item: item[1], reverse=True))

# enumerate makes it so we can get the index of the items stored in the dictionary
# this is paired with the medals in the list above
medals = ["🥇", "🥈", "🥉"]
for index, (name, points) in enumerate(points_data_sorted.items()):
    medal = f"{medals[index]}"
    st.markdown(f"# {medal}**{name}**: {points} points", text_alignment="center")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")