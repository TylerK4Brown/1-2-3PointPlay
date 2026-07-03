# Testing an API call and the parser altogether
# Gathers WNBA data from the Odds API, passes to display_data function, prints output to the console

import requests
import json
from parse_data import display_data

api_key = "YOUR_API_KEY_HERE"
sport_key = "basketball_wnba"
regions = 'us'
markets = "totals"
commence_timeFrom = '2026-07-02T22:34:00Z'
commence_timeTo = '2026-07-09T22:34:00Z'
api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={api_key}&markets={markets}&regions={regions}&commence_timeFrom={commence_timeFrom}&commence_timeTo={commence_timeTo}"

response = requests.get(api_url)
data = response.json()
# print(json.dumps(data, indent=2))

spread = 0
team_name = ""

display_data(data, spread, team_name)

    
    
    
    
    