# Either makes an API call to the Odds API or uses the data already stored in session state to display the upcoming MLB games and their point spreads

import requests
import json
import streamlit as st

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
        print(json.dumps(data, indent=2))
        display_data_mlb(data)

    # Otherwise, use the data stored in session state and display it
    else:
        # Debug statement to show it pulls data from the session state
        # print("API DATA ALREADY IN SESSION STATE - USING STORED DATA")
        display_data_mlb(st.session_state.api_data)

# Display the upcoming MLB games and O/U numbers
def display_data_mlb (data):
    over_under = None
    if "point_picks" not in st.session_state:
        st.session_state.point_picks = []

    st.markdown("### LISTING OF UPCOMING MLB GAMES AND THEIR POINT SPREADS", text_alignment="center")
    # hacky CSS to center expander text and make the font just a little bit larger
    st.markdown('''
    <style>
        [data-testid="stExpander"] div {
            display: flex;
            justify-content: center;
            font-size: 18px;
        }
                
        [data-testid="stExpander"] details {
            padding-bottom: 20px;
        }
        
        [data-testid="stCaptionContainer"] p {
            font-size: 25px;
        }
                
    </style>

    ''', unsafe_allow_html=True)

    for data_obj in data[0:8]:
        # skip an iteration if no bookmaker is listed for the game
        if len(data_obj["bookmakers"]) == 0:
            continue
        else:
            # create multiple expanders for each game
            # home and away team names displayed, plus the over/under number for the game
            home_team = data_obj["home_team"]
            away_team = data_obj["away_team"]
            col1, col2, col3 = st.columns([1, 5, 1])
            with col2:
                with st.expander(f'''{away_team} @ {home_team}, O/U: {data_obj['bookmakers'][0]['markets'][0]['outcomes'][0]['point']}''', expanded=False):
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.markdown("# VERSUS")

                    with col1:
                        st.image(f"images/{away_team.lower()}.png", width=200, caption=f"{away_team}")
                    with col3:
                        st.image(f"images/{home_team.lower()}.png", width=200, caption=f"{home_team}")

                    over_under = data_obj["bookmakers"][0]["markets"][0]["outcomes"][0]["point"]
                    # book = data_obj["bookmakers"][0]["key"]

                    st.markdown(f"## **O/U**: {over_under}", text_alignment='center')
                    # Create columns with an intentionally narrow middle column

        # center the segmented controls in the middle column
        # segmented control allows the user to make selections, and the key is stored in session state for tracking
        # on_change contains a reference to a callback function, args passes in the changed key upon change
        # allows us to edit states manually when the user clicks on buttons on the frontend
        with col2:
            st.segmented_control (
                label="over_under", 
                options=["OVER", "UNDER"], 
                key=f"{data_obj['home_team']}_OU", 
                width="stretch", 
                label_visibility="collapsed",
                on_change=handle_change,
                args=(f"{data_obj['home_team']}_OU", data,)
            )

            st.segmented_control (
                label="points", 
                options=["1", "2", "3"], 
                key=f"{data_obj['home_team']}_points", 
                width="stretch", 
                label_visibility="collapsed",
                on_change=handle_change,
                args=(f"{data_obj['home_team']}_points", data,)
            )

            st.divider(width=700)
    
# Callback function that handles changes to point values and updates states accordingly
def handle_change(changed_key, data):
    duplicate_exists = False
    # Split the changed key to get key type ("points" or "OU") and the home team name
    key_type = changed_key.split("_")[1]
    home_team_name = changed_key.split("_")[0]
    game_id = ""

    # get the game id for future API calls that will need to reference this game's information
    for data_obj in data:
        if data_obj['home_team'] == home_team_name:
            game_id = data_obj['id']
            break
    
    # If there are picks currently listed in the session state
    if st.session_state.point_picks:
        print("picks do exist in list")
        # check if the home team already exists in the point_picks list
        for pick in st.session_state.point_picks:
            print(f"for {pick} in the full list")
            # get the home team name for the current pick selected in the loop
            current_home_team_name = pick['home_team'].split("_")[0]
            same_name = False
            # if the name already exists in our list, update the point value and the flag that tracks duplicates
            print (f"{current_home_team_name} ------ {home_team_name}")
            if current_home_team_name == home_team_name:
                same_name = True
                duplicate_exists = True
                
                # check if the key type is points or OU and update the appropriate value in the session state
                if key_type == "points":
                    print("updating point value!")
                    pick['point_value'] = st.session_state[changed_key]
                elif key_type == "OU":
                    print("updating OU value!")
                    pick['over_under'] = st.session_state[changed_key]
            
            # If the point selection conflicts with another point selection, pop the old selection from the list
            # Does not check for a conflict if the name is the same
            if key_type == "points":
                if st.session_state[changed_key] == pick['point_value'] and not same_name:
                    print("different games with the same point value assignment - pop the old pick from the list")

                    # pop the entire pick from the list if there was no over/under value selected
                    # only append picks to the new session state list if that pick's point value is not equal to the selected point value
                    st.session_state.point_picks = [pick for pick in st.session_state.point_picks if pick["point_value"] != st.session_state[changed_key]]
                    # Recraft the original key so that it can be updated in the original session state that the buttons control
                    # i.e. "Arizona Diamondbacks" now goes to "Arizona Diamondbacks_points"
                    # Reset session state to None - deselects the button on the page
                    recrafted_key = pick['home_team'] + "_points"
                    recrafted_key2 = pick['home_team'] + "_OU"
                    st.session_state[recrafted_key2] = None
                    st.session_state[recrafted_key] = None

        # if there is no duplicate, append it to the running list of picks
        if not duplicate_exists:
            print("no duplicate exists - adding new value")
            add_new_pick_to_session_state(
                home_team_name, 
                st.session_state[changed_key] if key_type == "points" else None, 
                st.session_state[changed_key] if key_type == "OU" else None, 
                game_id
            )
    
        
    # otherwise, if there are no picks in the session state, append a new entry to the session state
    else:
        print("picks do not exist yet - add a new entry!")
        add_new_pick_to_session_state(
            home_team_name, 
            st.session_state[changed_key] if key_type == "points" else None, 
            st.session_state[changed_key] if key_type == "OU" else None, 
            game_id
        )
        
    # print for debugging
    print(json.dumps(st.session_state.point_picks, indent=2))

def add_new_pick_to_session_state(home_team_name, point_value, over_under, game_id):
    st.session_state.point_picks.append({
        "home_team": home_team_name,
        "point_value": point_value,
        "over_under": over_under,
        "game_id": game_id
    })

# For later when we're gonna go week by week for the NFL
def calculate_date_time():
    pass