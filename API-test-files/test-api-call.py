# Testing an API call and the parser altogether
# Gathers WNBA data from the Odds API, passes to display_data function, prints output to the console

import requests
import json
from parse_data import display_data_wnba, display_data_mlb

api_key = "apikey"
# sport_key = "baseball_mlb"
# bookmakers = "espnbet"
# markets = "totals"
# commence_timeFrom = '2026-07-02T22:34:00Z'
# commence_timeTo = '2026-07-09T22:34:00Z'
# api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={api_key}&markets={markets}&bookmakers={bookmakers}&commence_timeFrom={commence_timeFrom}&commence_timeTo={commence_timeTo}"

# response = requests.get(api_url)
# data = response.json()
# # print(json.dumps(data, indent=2))

# display_data_mlb(data)

sport_key = "basketball_wnba"
daysFrom = 3
commence_timeFrom = '2025-09-20T22:34:00Z'
commence_timeTo = '2025-09-30T22:34:00Z'

api_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/scores/?apiKey={api_key}&daysFrom={daysFrom}"

response = requests.get(api_url)
data = response.json()

print(json.dumps(data, indent=2))
    
    
    
    
    