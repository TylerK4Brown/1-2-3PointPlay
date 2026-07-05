# Either makes an API call to the Odds API or uses the data already stored in session state to display the upcoming MLB games and their point spreads

import requests
import json
import streamlit as st
import API_info.display_data as display_data

def make_api_call():
    
    # If API data is not in the session state, make an API call
    if "api_data" not in st.session_state:
        # Initialize session state to none at first
        st.session_state.api_data = None
        api_key = "fbd28c927419891b76b59b6528531cd2"
        sport_key = "baseball_mlb"
        bookmakers = "espnbet"
        markets = "totals"
        commence_timeFrom = '2026-07-02T22:34:00Z'
        commence_timeTo = '2026-07-09T22:34:00Z'

        api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={api_key}&markets={markets}&bookmakers={bookmakers}&commence_timeFrom={commence_timeFrom}&commence_timeTo={commence_timeTo}"

        response = requests.get(api_url)
        data = response.json()

        st.session_state.api_data = data
        # Debug statements to check if the API call was successful
        # print("API CALL MADE - INFORMATION STORED IN SESSION STATE")
        # print(json.dumps(data, indent=2))
        display_data.display_data_mlb(data)

    # Otherwise, use the data stored in session state and display it
    else:
        # Debug statement to show it pulls data from the session state
        # print("API DATA ALREADY IN SESSION STATE - USING STORED DATA")
        display_data.display_data_mlb(st.session_state.api_data)