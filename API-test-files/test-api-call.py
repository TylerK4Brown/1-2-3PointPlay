# Testing an API call and the parser altogether
# Gathers WNBA data from the Odds API, passes to display_data function, prints output to the console

import requests
import json
from parse_data import display_data_wnba, display_data_mlb

api_key = "YOUR_API_KEY"
sport_key = "baseball_mlb"
bookmakers = "espnbet"
markets = "totals"
commence_timeFrom = '2026-07-02T22:34:00Z'
commence_timeTo = '2026-07-09T22:34:00Z'
api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={api_key}&markets={markets}&bookmakers={bookmakers}&commence_timeFrom={commence_timeFrom}&commence_timeTo={commence_timeTo}"

response = requests.get(api_url)
data = response.json()
# print(json.dumps(data, indent=2))

display_data_mlb(data)

    
    
    
    
    