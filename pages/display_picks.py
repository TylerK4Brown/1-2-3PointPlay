# Display user's picks on a new page when they click submit
import streamlit as st

# if these are not in the session state, redirect the user back to the landing page
# selecting a name in the landing page will initialize these session states
if "name" not in st.session_state or "point_picks" not in st.session_state:
    st.title("NAME NOT SELECTED - PLEASE RETURN TO THE LANDING PAGE AND SELECT A NAME", text_alignment="center")

# otherwise, iterate through the custom dictionary and display the user's picks
else:
    st.title(f"Here are your picks, {st.session_state.name}!", text_alignment="center")
    st.divider(width='stretch')
    for pick in st.session_state.point_picks:
        # Only display picks that have been fully filled out (point value and over/under selected)
        if pick['point_value'] is None or pick['over_under'] is None:
            continue
        else:
            st.markdown(f"### {pick['away_team']} @ {pick['home_team']}", text_alignment="center")
            st.markdown(f"#### Your pick: {pick['over_under']} (O/U: {pick['over_under_score']})", text_alignment="center")
            st.markdown(f"#### Points: {pick['point_value']}", text_alignment="center")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.divider(width='stretch')
    
# centered return to landing page button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Continue Making Picks", width=700, key="continue_making_picks"):
        st.switch_page("pages/make_your_picks.py")

    if st.button("Return to Landing Page", width=700, key="return_landing_page"):
        st.switch_page("pages/landing_page.py")