# Contains a few API endpoint tests that are used to visualize the JSON output of the call

import requests
import json

# Default endpoint that returns all sports
api_key = "api_key"
default_api = f"https://api.the-odds-api.com/v4/sports/?apiKey={api_key}"

commence_timeFrom = '2026-09-09T22:34:00Z'
commence_timeTo = "2026-09-16T22:34:00Z"
markets = 'spreads'
bookmakers = "espnbet"

# Returns all NFL preseason events within the above time frame
return_all_events = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={api_key}&markets={markets}&commenceTimeFrom={commence_timeFrom}&commenceTimeTo={commence_timeTo}&bookmakers={bookmakers}"

response = requests.get(return_all_events)
data = response.json()
print(json.dumps(data, indent=2))