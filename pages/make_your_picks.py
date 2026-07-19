# Picks page for the app
# Makes an API call to The Odds API to get the games for the week, and displays them in Streamlit expander elements
import streamlit as st
from API_info.odds_api_call import make_api_call
from default_behavior import check_session_states

# Makes sure all proper state variables are present before starting
if check_session_states():
    st.title(f"Player selected: {st.session_state.name}", text_alignment="center")
    # set a disabled state for the segmented controls buttons that are created in the display_data_mlb function.
    if "disabled" not in st.session_state:
        st.session_state.disabled = True
    
    # Make API call, which also displays the games for the week
    make_api_call()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # add spacing between expander and button
        if "name" in st.session_state and "point_picks" in st.session_state:
            st.markdown("")
            st.markdown("")
            if st.button("View Your Picks", width=700, key="view_picks", type="primary"):
                st.switch_page("pages/display_picks.py")

    # centered return to landing page button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # add spacing between buttons
        st.markdown("")
        st.markdown("")
        if st.button("Return to Landing Page", width=700, key="return_landing_page"):
            st.switch_page("pages/landing_page.py")