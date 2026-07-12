# Testing an API call and the parser altogether
# Gathers WNBA data from the Odds API, passes to display_data function, prints output to the console

import requests
import json
from parse_data import display_data_wnba, display_data_mlb
import streamlit as st

api_key = st.secrets["OddsAPI_key"]
sport_key = "americanfootball_nfl"
bookmakers = "espnbet"
markets = "spreads"
commence_timeFrom = '2026-08-13T22:59:00Z'
commence_timeTo = '2026-08-16T00:00:00Z'
api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={api_key}&markets={markets}&bookmakers={bookmakers}&commenceTimeFrom={commence_timeFrom}&commenceTimeTo={commence_timeTo}"

response = requests.get(api_url)
data = response.json()
print(json.dumps(data, indent=2))

# display_data_mlb(data)

# sport_key = "americanfootball_nfl_preseason"
# daysFrom = 3
# commence_timeFrom = '2025-09-20T22:34:00Z'
# commence_timeTo = '2025-09-30T22:34:00Z'

# api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/scores/?apiKey={api_key}&daysFrom={daysFrom}"

# response = requests.get(api_url)
# data = response.json()

# print(json.dumps(data, indent=2))
    
    
    
    
    