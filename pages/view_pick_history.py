import streamlit as st
from database_operations.database import get_picks_by_week, get_week_number

if "player_history_selected" not in st.session_state:
    st.session_state.player_history_selected = None
    
st.markdown("# Pick History", text_alignment="center")
st.divider(width='stretch')

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

if st.session_state.player_history_selected is None:
    st.markdown("## Please select a player to view their pick history.", text_alignment="center")
else:
    st.markdown(f"## Viewing pick history for {st.session_state.player_history_selected}", text_alignment="center")


