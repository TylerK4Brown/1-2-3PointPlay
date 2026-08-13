## statistics.py
## Computes and displays aggregate pick performance statistics across users and weeks
## Includes one helper function for all-time spread coverage summaries
## Eventually, this page will also include buttons to view per-player statistics and trend breakdowns

import streamlit as st
from database_operations.database import get_picks_by_week, get_week_number

# Get totals for picks covering the spread for all users for a given week or weeks
def get_pick_statistics(week_number):
    # if week number isn't a list, convert to a list so it can be iterated
    if not isinstance(week_number, list):
        week_number = [week_number]

    total_picks_covering = 0
    one_point_picks_covering = 0
    two_point_picks_covering = 0
    three_point_picks_covering = 0

    for week in week_number:
        rows = get_picks_by_week(week, None)
        # 3 rows get returned, one for each user.
        # Each row contains a picks list for that week.
        # Iterate through each row and then through each pick list to count
        # the number of picks covering the spread.
        for row in rows:
            for picks in row[f"week_{week}"]["picks"]:
                if picks["covering_spread"]:
                    total_picks_covering += 1

                    if picks["point_value"] == "1":
                        one_point_picks_covering += 1
                    elif picks["point_value"] == "2":
                        two_point_picks_covering += 1
                    elif picks["point_value"] == "3":
                        three_point_picks_covering += 1

    # return information in a dictionary to be used in the statistics page
    return {
        "total_picks_covering": total_picks_covering,
        "one_point_picks_covering": one_point_picks_covering,
        "two_point_picks_covering": two_point_picks_covering,
        "three_point_picks_covering": three_point_picks_covering,
    }


# Display statistics on the statistics page
st.markdown("# Overall Statistics", text_alignment="center")
st.divider(width='stretch')

week_number = get_week_number()
week_number -= 1

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
if week_number > 1:
    week_number = [i for i in range(1, week_number + 1)]

week_being_considered = week_number
if isinstance(week_number, list):
    week_being_considered = week_number[-1]

# Begin the display of statistics for all weeks that have passed
total_possible_picks = week_being_considered * 9
total_possible_point_plays = week_being_considered * 3
pick_statistics = get_pick_statistics(week_number)
total_picks_covering = pick_statistics["total_picks_covering"]
one_point_picks_covering = pick_statistics["one_point_picks_covering"]
two_point_picks_covering = pick_statistics["two_point_picks_covering"]
three_point_picks_covering = pick_statistics["three_point_picks_covering"]

st.markdown(f"# Total picks correct: {total_picks_covering} / {total_possible_picks} ({((total_picks_covering / total_possible_picks) * 100):.1f}%)", text_alignment="center")
st.divider(width='stretch')

st.markdown(f"# 1 point picks correct: {one_point_picks_covering} / {total_possible_point_plays} ({((one_point_picks_covering / total_possible_point_plays) * 100):.1f}%)", text_alignment="center")
st.markdown(f"# 2 point picks correct: {two_point_picks_covering} / {total_possible_point_plays} ({((two_point_picks_covering / total_possible_point_plays) * 100):.1f}%)", text_alignment="center")
st.markdown(f"# 3 point picks correct: {three_point_picks_covering} / {total_possible_point_plays} ({((three_point_picks_covering / total_possible_point_plays) * 100):.1f}%)", text_alignment="center")
st.divider(width='stretch')

newcol1, newcol2, newcol3 = st.columns([1, 1, 1])
with newcol2:
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")

