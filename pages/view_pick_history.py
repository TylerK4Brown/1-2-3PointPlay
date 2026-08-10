import streamlit as st
from database_operations.database import get_picks_by_week, get_week_number, get_point_total_for_week, get_win_loss_by_week
from display_helpers.view_picks import display_player_picks
from display_helpers.number_formatting import format_points
from css.streamlit_css import load_css_gamedisplay

# Callback function for the slider to save the selected week range in session state
# Helps with persistence of the slider's value when a button is clicked to view a different player's pick history
def save_week_slider_range():
    st.session_state.week_slider_saved = st.session_state.week_slider

load_css_gamedisplay()
if "player_history_selected" not in st.session_state:
    st.session_state.player_history_selected = None
    
st.markdown("# Pick History", text_alignment="center")
st.divider(width='stretch')

# Get the week number minus 1, current week does not count towards the history
week_number = get_week_number()
week_number -= 1

if "week_slider_saved" not in st.session_state:
    st.session_state.week_slider_saved = (1, week_number)

# Buttons to view different player's pick histories
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("View Dad's Pick History", width='stretch', key="view_dad_history"):
        st.session_state.player_history_selected = "Dad"
        st.rerun()
with col2:
    if st.button("View TJ's Pick History", width='stretch', key="view_tj_history"):
        st.session_state.player_history_selected = "TJ"
        st.rerun()
with col3:
    if st.button("View Tyler's Pick History", width='stretch', key="view_tyler_history"):
        st.session_state.player_history_selected = "Tyler"
        st.rerun()

# A slider to view a range of weeks for the pick history
# Only appears of at least 2 weeks have passed in the season
slidercol1, slidercol2, slidercol3 = st.columns([1, 1, 1])
with slidercol2:
    if week_number >= 2:
        # Slider operates off of the last saved value in session state
        # If there isn't a value, it defaults to the max range of weeks that have passed
        # Otherwise, it uses the saved value to ensure persistence of the slider's range when displaying player pick history
        if "week_slider" not in st.session_state:
            st.session_state.week_slider = st.session_state.week_slider_saved

        st.slider(
            "Select Week Range",
            min_value=1,
            max_value=week_number,
            value=st.session_state.week_slider_saved,
            key="week_slider",
            step=1,
            on_change=save_week_slider_range,
        )

# Text to display which player's pick history is being viewed, or a message to select a player if none has been selected yet
if st.session_state.player_history_selected is None:
    st.markdown("## Please select a player to view their pick history.", text_alignment="center")
else:
    st.markdown(f"## Viewing pick history for {st.session_state.player_history_selected}", text_alignment="center")
    st.divider(width='stretch')

# If a player has been selected, display their pick history for the selected range
if st.session_state.player_history_selected is not None:
    # If no weeks have passed, display a message to check back after the first week of the season
    if week_number < 1:
        st.markdown("## No pick history available yet. Please check back after the first week of the season.", text_alignment="center")
    else:
        # if more than 1 week has passed, create array of multiple weeks to display pick history for all weeks that have passed
        # grabs the range from the slider if the slider has been created
        # otherwise, create a list and put only week 1 in it so that the for loop below can iterate through it and display the pick history for week 1
        if week_number >= 2:
            if "week_slider" in st.session_state:
                st.session_state.week_slider_saved = st.session_state.week_slider
            week_range = list(range(st.session_state.week_slider_saved[0], st.session_state.week_slider_saved[1] + 1))
        else:
            week_range = [1]

        # for each week in the range, get the picks by week from the database and display them using the display_player_picks display helper
        for week in week_range:
            week_total = 0
            accumulated_points_on_this_week = get_point_total_for_week(week, st.session_state.player_history_selected)
            win_loss_data = get_win_loss_by_week(week, st.session_state.player_history_selected)
            st.markdown(f"### Week {week} Picks", text_alignment="center")
            rows = get_picks_by_week(week, st.session_state.player_history_selected)
            picks = rows[0][f"week_{week}"]["picks"]
            for pick in picks:
                home_team = pick["home_team"]
                away_team = pick["away_team"]
                game_spread = pick["original_spread"]
                spread_pick = pick["spread_pick"]
                point_value = pick["point_value"]
                score_home_team = pick["home_team_score"]
                score_away_team = pick["away_team_score"]
                covering_spread = pick["covering_spread"]

                # Display the player's picks using the display_player_picks function
                display_player_picks(home_team, away_team, game_spread, point_value, spread_pick, score_home_team, score_away_team, covering_spread)
                if covering_spread == True:
                    week_total += float(point_value)
                if covering_spread == "push":
                    week_total += float(point_value) / 2

            st.markdown(f"### Points Earned This Week: {format_points(week_total)}", text_alignment="center")
            st.markdown(f"### Total Points Accumulated: {format_points(accumulated_points_on_this_week)}", text_alignment="center")
            if win_loss_data['picks_push'] == 0:
                st.markdown(f"### W/L Record: {win_loss_data['picks_correct']} - {win_loss_data['picks_incorrect']}", text_alignment="center")
            else:
                st.markdown(f"### W/L Record: {win_loss_data['picks_correct']} - {win_loss_data['picks_incorrect']} - {win_loss_data['picks_push']}", text_alignment="center")
            st.divider(width='stretch')

# centered return to landing page button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    # add spacing between buttons
    st.markdown("")
    st.markdown("")
    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")