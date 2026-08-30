## statistics.py
## Computes and displays aggregate pick performance statistics across users and weeks
## Includes one helper function for all-time spread coverage summaries
## Eventually, this page will also include buttons to view per-player statistics and trend breakdowns

import streamlit as st
from css.streamlit_css import load_css_gamedisplay
from database_operations.database import get_picks_by_week, get_week_number
from display_helpers.stat_gathering import get_pick_statistics

load_css_gamedisplay()
week_number = get_week_number()
week_number -= 1
week_being_considered = week_number
# Display statistics on the statistics page
st.markdown("# Overall Statistics", text_alignment="center")
st.divider(width='stretch')
# If at least 1 week has not passed, display no stats
if week_number < 1:
    st.markdown("# No statistics available yet. Please check back after the first week of the season.", text_alignment="center")
    st.divider(width='stretch')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Return to Landing Page", width=700, key="return_landing_page"):
            st.switch_page("pages/landing_page.py")
    st.stop()

# if more than 1 week has passed, create array of multiple weeks to display statistics for all weeks that have passed
# If only one week has passed, the display helper function will convert it into a list to be iterated across
if week_number > 1:
    week_number = [i for i in range(1, week_number + 1)]

# Begin the display of statistics for all weeks that have passed
total_possible_picks = week_being_considered * 9
total_possible_point_plays = week_being_considered * 3
pick_statistics = get_pick_statistics(week_number, "overall")
total_picks_covering = pick_statistics["total_picks_covering"]
one_point_picks_covering = pick_statistics["one_point_picks_covering"]
two_point_picks_covering = pick_statistics["two_point_picks_covering"]
three_point_picks_covering = pick_statistics["three_point_picks_covering"]
most_frequent_teams_picked = pick_statistics["most_frequent_teams_picked"]

st.markdown(f"# Total picks correct: :blue[{total_picks_covering} / {total_possible_picks} ({((total_picks_covering / total_possible_picks) * 100):.1f}%)]", text_alignment="center")
st.divider(width='stretch')

st.markdown(f"# 1 point picks correct: :blue[{one_point_picks_covering} / {total_possible_point_plays} ({((one_point_picks_covering / total_possible_point_plays) * 100):.1f}%)]", text_alignment="center")
st.markdown(f"# 2 point picks correct: :blue[{two_point_picks_covering} / {total_possible_point_plays} ({((two_point_picks_covering / total_possible_point_plays) * 100):.1f}%)]", text_alignment="center")
st.markdown(f"# 3 point picks correct: :blue[{three_point_picks_covering} / {total_possible_point_plays} ({((three_point_picks_covering / total_possible_point_plays) * 100):.1f}%)]", text_alignment="center")
st.divider(width='stretch')

st.markdown("## :blue[Top 3 Most Frequently Picked Teams]", text_alignment="center")
# Sort teams by the number of times they were picked in descending order (-team[1])
# Uses a secondary sort to break ties alphabetically by team name (team[0])
sorted_most_frequent_teams = sorted(most_frequent_teams_picked.items(), key=lambda team: (-team[1], team[0]))
for index, (team, count) in enumerate(sorted_most_frequent_teams):
    if index >= 3:
        break
    st.markdown(f"#### {team}: {count} times", text_alignment="center")

newcol1, newcol2, newcol3 = st.columns([1, 1, 1])
with newcol2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")

