# Contains a few API endpoint tests that are used to visualize the JSON output of the call

import requests
import json

# Default endpoint that returns all sports
api_key = "YOUR_API_KEY_HERE"
default_api = f"https://api.the-odds-api.com/v4/sports/?apiKey={api_key}"

commence_timeFrom = '2026-07-02T22:34:00Z'
commence_timeTo = '2026-07-09T22:34:00Z'

# Returns all MLB events within the above time frame
return_all_events = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/events?apiKey={api_key}&commence_timeFrom={commence_timeFrom}&commence_timeTo={commence_timeTo}"

response = requests.get(return_all_events)
data = response.json()
print(json.dumps(data, indent=2))