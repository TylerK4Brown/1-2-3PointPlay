# Either makes an API call to the Odds API or uses the data already stored in session state to display the upcoming MLB games and their point spreads

import requests
import json
import streamlit as st
import API_info.display_data as display_data
from database_operations.database import get_week_number
from dictionaries.week_info import NFL_2026_WEEK_TIME_WINDOWS

def make_api_call():
    
    # If API data is not in the session state, make an API call
    if "api_data" not in st.session_state:
        # Initialize session state to none at first
        st.session_state.api_data = None
        api_key = st.secrets["OddsAPI_key"]
        # sport_key = "americanfootball_nfl_preseason"
        sport_key = "americanfootball_nfl"
        bookmakers = "draftkings"
        markets = "spreads"
        daysFrom = 3
        # Grab week number from the database, compare it to the dictionary of week + time windows
        # Use those values to complete the API call
        current_week_number = get_week_number()
        commence_timeFrom = NFL_2026_WEEK_TIME_WINDOWS[current_week_number]["commence_timeFrom"]
        commence_timeTo = NFL_2026_WEEK_TIME_WINDOWS[current_week_number]["commence_timeTo"]

        api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={api_key}&markets={markets}&bookmakers={bookmakers}&commenceTimeFrom={commence_timeFrom}&commenceTimeTo={commence_timeTo}&daysFrom={daysFrom}"

        response = requests.get(api_url)
        data = response.json()

        st.session_state.api_data = data
        # Debug statements to check if the API call was successful
        # print("API CALL MADE - INFORMATION STORED IN SESSION STATE")
        display_data.display_data_nfl(data)

    # Otherwise, use the data stored in session state and display it
    else:
        # Debug statement to show it pulls data from the session state
        # print("API DATA ALREADY IN SESSION STATE - USING STORED DATA")
        display_data.display_data_nfl(st.session_state.api_data)

# Making an API call to the scores API to get the scores for a specific game ID
def make_scores_api_call(event_id_list):
    api_key = st.secrets["OddsAPI_key"]
    sport_key = "americanfootball_nfl"
    api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/scores/?apiKey={api_key}&eventIds={','.join(event_id_list)}"
    
    response = requests.get(api_url)
    data = response.json()

    return data