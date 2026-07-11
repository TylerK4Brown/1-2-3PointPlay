# Either makes an API call to the Odds API or uses the data already stored in session state to display the upcoming MLB games and their point spreads

import requests
import json
import streamlit as st
from API_info.display_data import display_data_mlb

def make_api_call():
    
    # If API data is not in the session state, make an API call
    if "api_data" not in st.session_state:
        # Initialize session state to none at first
        st.session_state.api_data = None
        api_key = st.secrets["OddsAPI_key"]
        sport_key = "baseball_mlb"
        bookmakers = "espnbet"
        markets = "totals"
        commence_timeFrom = '2026-07-11T22:10:00Z'
        commence_timeTo = '2026-07-12T04:00:00Z'

        api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={api_key}&markets={markets}&bookmakers={bookmakers}&commenceTimeFrom={commence_timeFrom}&commenceTimeTo={commence_timeTo}"

        response = requests.get(api_url)
        data = response.json()

        st.session_state.api_data = data
        # Debug statements to check if the API call was successful
        # print("API CALL MADE - INFORMATION STORED IN SESSION STATE")
        display_data_mlb(data)

    # Otherwise, use the data stored in session state and display it
    else:
        # Debug statement to show it pulls data from the session state
        # print("API DATA ALREADY IN SESSION STATE - USING STORED DATA")
        display_data_mlb(st.session_state.api_data)

# Making an API call to the scores API to get the scores for a specific game ID
def make_scores_api_call(event_id_list):
    api_key = st.secrets["OddsAPI_key"]
    sport_key = "baseball_mlb"
    string_event_ids = ','.join(event_id_list)
    print(f"MAKING API CALL TO ODDS API FOR GAME SCORES | EVENT ID LIST: {string_event_ids}")
    api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/scores/?apiKey={api_key}&eventIds={','.join(event_id_list)}"
    
    response = requests.get(api_url)
    data = response.json()

    return data