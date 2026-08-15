## odds_api_call.py
## Handles API requests to retrieve weekly game odds and live score information
## Applies date-window filtering and stores responses in session state for page rendering

# Either makes an API call to the Odds API or uses the data already stored in session state to display the upcoming MLB games and their point spreads

import requests
import streamlit as st
from database_operations.database import get_week_number
from dictionaries.week_info import NFL_2026_WEEK_TIME_WINDOWS

def make_api_call():
    # Initialize session state to none at first
    st.session_state.game_data = None
    api_key = st.secrets["OddsAPI_key"]
    # sport_key = "americanfootball_nfl_preseason"
    sport_key = "americanfootball_nfl_preseason"
    bookmakers = "draftkings"
    markets = "spreads"
    daysFrom = 3
    # Grab week number from the database, compare it to the dictionary of week + time windows
    # Use those values to complete the API call
    # Store in session state so it can be used elsewhere
    current_week_number = get_week_number()
    if "week_number" not in st.session_state:
        st.session_state.week_number = current_week_number
    commence_timeFrom = NFL_2026_WEEK_TIME_WINDOWS.get(current_week_number, {}).get("commence_timeFrom")
    commence_timeTo = NFL_2026_WEEK_TIME_WINDOWS.get(current_week_number, {}).get("commence_timeTo")

    api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={api_key}&markets={markets}&bookmakers={bookmakers}&commenceTimeFrom={commence_timeFrom}&commenceTimeTo={commence_timeTo}&daysFrom={daysFrom}"

    response = requests.get(api_url)
    data = response.json()
    st.session_state.game_data = data

# Making an API call to the scores API to get the scores for a specific game ID
def make_scores_api_call(event_id_list):
    api_key = st.secrets["OddsAPI_key"]
    sport_key = "americanfootball_nfl_preseason"
    api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/scores/?apiKey={api_key}&eventIds={','.join(event_id_list)}"
    
    response = requests.get(api_url)
    data = response.json()

    return data