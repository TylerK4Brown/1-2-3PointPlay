import streamlit as st
from database_operations.database import get_picks_by_week, get_week_number

# 
def get_pick_statistics(week_number):
    rows = get_picks_by_week(week_number)
    total_picks_covering = 0
    one_point_picks_covering = 0
    two_point_picks_covering = 0
    three_point_picks_covering = 0

    # 3 rows get returned, one for each user
    # Each row contains a picks list for that week
    # Iterate through each row and then through each pick list to count number of picks covering the spread
    for row in rows:
        for picks in row[f"week_{week_number}"]["picks"]:
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
        "three_point_picks_covering": three_point_picks_covering
    }


# Display statistics on the statistics page
st.markdown("# fun stats I guess :smile:", text_alignment="center")
st.divider(width='stretch')

week_number = get_week_number()
week_number -= 1
total_possible_picks = week_number * 9
total_possible_point_plays = week_number * 3

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
