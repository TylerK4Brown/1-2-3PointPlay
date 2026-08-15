## display_data.py
## Takes information from the API call and displays it to the user using Streamlit expanders
## When the user clicks on an expander, it will reveal a spread selection and point value selection
## Callback function handles changes to selections and updates the session state accordingly

import streamlit as st
from css.streamlit_css import load_css_gamedisplay
from dictionaries.games_per_week import NFL_GAMES_PER_WEEK
from dictionaries.abbreviation_mapping import ABBREVIATION_MAPPING, REVERSED_ABBREVIATION_MAPPING
import json
from datetime import datetime
from zoneinfo import ZoneInfo

# Display the upcoming NFL games and point spreads
def display_data_nfl (data):
    button_id = 1
    week_number = st.session_state.week_number

    # Checks to make sure the length of the data returned from the API call is the expected number
    # If not, this probably means that an older game is no longer returned by the API (i.e, a game played on Wednesday this week will be removed from the API call on Sunday morning)
    # To avoid a mismatch between the button IDs and the game information, increment the button ID
    # This allows for the button IDs to match the game information in session state and in the database
    if len(data) < NFL_GAMES_PER_WEEK[week_number]:
        increment_button_id = NFL_GAMES_PER_WEEK[week_number] - len(data)
        button_id += increment_button_id
    # create the game_information list in session state if it doesn't already exist
    if "game_information" not in st.session_state:
        st.session_state.game_information = []
    
    # reset session state for game information if it already exists
    # clicking on buttons rerenders the entire page, which would cause this list to grow indefinitely
    # since we append to this list each time a button is clicked
    if "game_information" in st.session_state:
        st.session_state.game_information = []

    # load hacky CSS that messes with the expander element display
    load_css_gamedisplay()
    # checks if the user has already made picks in this session - updates state accordingly
    buttons_already_selected()

    st.markdown("### LISTING OF UPCOMING NFL GAMES AND THEIR POINT SPREADS", text_alignment="center")
    start_times_list = []
    for data_obj in data:
        # skip an iteration if no bookmaker is listed for the game
        if len(data_obj["bookmakers"]) == 0:
            continue
        else:
            generate_expander(data_obj, button_id, start_times_list)
            button_id += 1

# Generate expander elements for each game made available from the API call
def generate_expander(data_obj, button_id, start_times_list):
    # extract home team, away team, point spreads for the favored and underdog teams, and the game ID from the API call data
    # also call the abbreviation mapping function for later use in the expander display
    home_team = data_obj["home_team"]
    away_team = data_obj["away_team"]
    home_team_abbreviation = ABBREVIATION_MAPPING[home_team]
    away_team_abbreviation = ABBREVIATION_MAPPING[away_team]
    start_time = data_obj["commence_time"]
    point_spread = data_obj["bookmakers"][0]["markets"][0]["outcomes"]
    game_id = data_obj['id']
    team_favored, team_favored_abbreviation, point_spread_favored, team_underdog, team_underdog_abbreviation, point_spread_underdog = None, None, None, None, None, None
    is_spread_even = False

    # iterate through the point_spread list to find the favored and underdog teams and their respective point spreads
    for spread in point_spread:
        if spread["point"] == 0:
            is_spread_even = True
            home_team_abbreviation = ABBREVIATION_MAPPING[home_team]
            away_team_abbreviation = ABBREVIATION_MAPPING[away_team]
        if spread["point"] < 0:
            team_favored = spread["name"]
            team_favored_abbreviation = ABBREVIATION_MAPPING[team_favored]
            point_spread_favored = spread["point"]
        if spread["point"] > 0:
            team_underdog = spread["name"]
            team_underdog_abbreviation = ABBREVIATION_MAPPING[team_underdog]
            point_spread_underdog = spread["point"]

    point_spread = f"{team_favored_abbreviation} {point_spread_favored}" if not is_spread_even else "EVEN"

    # create a new entry in the session state for the game
    add_new_game_information_to_session_state(button_id, game_id, home_team, away_team, point_spread, team_favored, start_time)
    start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/New_York")).strftime('%A, %B %d')
    # Start times list: instantiate before iterating through each expander generation
    # Starts off empty - appends new start times and writes them on the page as they're encountered
    if len(start_times_list) == 0:
        st.divider(width='stretch')
        start_times_list.append(start_time)
        st.markdown(f"### :blue[{start_time}]", text_alignment='center')
        
    # If the start_times_list is not empty, iterate through the list to see if a duplicate entry exists. 
    # If a duplicate entry exists, break the loop and do not display it to the page
    else:
        for previous_start_times in start_times_list:
            if start_time == previous_start_times:
                break
            
        # If the date/time combination doesn't exist, append it to the list and display it to the page
        else:
            st.divider(width='stretch')
            start_times_list.append(start_time)
            st.markdown(f"### :blue[{start_time}]", text_alignment='center')

    # Start generating the expanders for each game in the current week
    col1, col2, col3 = st.columns([1, 7, 1])
    with col2:
        if is_spread_even:
            expander_string = (
                f"{away_team} @ {home_team}\n"
                f"Spread: EVEN"
            )
        else:
            expander_string = (
                f"{away_team} @ {home_team}\n"
                f"Spread: {team_favored_abbreviation} {point_spread_favored}"
            )
        with st.expander(expander_string, expanded=False):
            # create columns within the expander to display team logs
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.image(f"images_nfl/{away_team.lower()}.png", width=100)
                
            with col2:  
                st.title(f"@", text_alignment='center') 
            with col3:
                st.image(f"images_nfl/{home_team.lower()}.png", width=100)
            
            # display the date and time of the game 
            # display the spread for the game
            if is_spread_even:
                st.markdown(f"## **SPREAD**: EVEN", text_alignment='center')
            else:
                st.markdown(f"## **SPREAD**: {team_favored_abbreviation} {point_spread_favored}", text_alignment='center')
            
            # Create columns with an intentionally narrow middle column
            # center the segmented controls in the middle column
            # segmented control allows the user to make selections, and the key is stored in session state for tracking
            # on_change contains a reference to a callback function, args passes in the changed key upon change
            # allows us to edit states manually when the user clicks on buttons on the frontend
            if is_spread_even:
                options_list = [f"{home_team_abbreviation}", f"{away_team_abbreviation}"]
            else:
                options_list = [f"{team_favored_abbreviation} {point_spread_favored}", f"{team_underdog_abbreviation} +{point_spread_underdog}"]
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.segmented_control (
                    label="spread", 
                    options=options_list, 
                    key=f"{button_id}_spread", 
                    width="stretch", 
                    label_visibility="collapsed",
                    on_change=handle_change,
                    args=(f"{button_id}_spread", st.session_state.game_information,)
                )

                st.segmented_control (
                    label="points", 
                    options=["1", "2", "3"], 
                    key=f"{button_id}_points", 
                    width="stretch", 
                    label_visibility="collapsed",
                    on_change=handle_change,
                    args=(f"{button_id}_points", st.session_state.game_information,)
                )
                
                st.divider(width='stretch')
            
# Callback function that handles changes to point values and updates states accordingly
# changed_key = "<button_id>_<key_type>" (e.g., "1_points" or "2_spread")
# game_info is a list of dictionaries containing information about each game from the API call
def handle_change(changed_key, game_info):

    # -- INITIAL INFORMATION GATHERING, TWO PARTS --
    
    # PART 1: Grab information about the button that was clicked
    # 1. key_type = points or spread (key_type is in the format "<button_id>_<key_type>", so we split it to get the key_type)
    # 2. button_id = the ID of the button that was clicked (used to find the game information in the game_info list)
    # 3. value_of_pick = the value of the pick that was selected (e.g., "1", "2", "3" for points or "<team_abbreviation> <spread_value>" for spread)
    key_type = changed_key.split("_")[1]
    button_id = int(changed_key.split("_")[0])
    value_of_pick = st.session_state[changed_key]
    game = game_info[button_id - 1]
    start_time = game["start_time"]
    original_spread = game["spread"]

    # PART 2: Check if a game has already started
    # If the game has started, reset the button state to None and display a message to the user
    if start_time < datetime.now().isoformat():
        st.toast(f"PICK DENIED: Cannot make changes to a game that has already started.", icon="⚠️", duration=5)
        # reset the button state to None - deselects the button on the page
        st.session_state[changed_key] = None
        return

    # PART 3: Check if this pick selection has been finalized in the database
    # Does two checks:
    # 1. If the button ID matches an existing pick in the session state, reset the button states to their selected values
    # 2. If the point value matches an existing pick in the session state, reset the pick made to None
    for pick in st.session_state.point_picks:
        if pick["is_pick_in_database"] == False:
            continue

        # check 1
        if pick["button_id"] == button_id and pick["is_pick_in_database"] == True:
            st.toast(f"Cannot change a pick that has already been finalized. Please tell Tyler if you need to make changes.", icon="⚠️", duration=5)
            # reset the button state to None - deselects the button on the page
            st.session_state[changed_key] = value_of_pick
            return
        # check 2
        elif key_type == "points" and pick["point_value"] == value_of_pick:
            st.toast(f"{pick['point_value']} point play has already been finalized. Please assign a different point value to this game.", icon="⚠️", duration=5)
            # reset the button state to None - deselects the button on the page
            st.session_state[changed_key] = None
            return

    # PART 4: Grab information about the game that corresponds to that button ID from the game_info list
    home_team_name = game["home_team"]
    away_team_name = game["away_team"]
    game_id = game["game_id"]
    start_time = game["start_time"]
    is_pick_home = False
    
    # If the key type is spread, determine if the pick is for the home team or the away team
    # This helps later when we are calculating if the pick covered the spread or not
    # Does a null check since this would also run if the user deselects a spread pick
    if key_type == "spread" and value_of_pick is not None:
        spread_pick = value_of_pick
        pick_abbreviation = spread_pick.split(" ")[0]
        if REVERSED_ABBREVIATION_MAPPING[pick_abbreviation] == home_team_name:
            is_pick_home = True
    
    # -- UPDATE SESSION STATE BASED ON THE INFORMATION GATHERED ABOVE --
    # PART 1: If there are no picks in the session state, add a new entry
    if not st.session_state.point_picks:
        add_new_pick_to_session_state(
            home_team_name, 
            away_team_name,
            value_of_pick if key_type == "points" else None, 
            value_of_pick if key_type == "spread" else None,
            is_pick_home,
            game_id,
            button_id,
            start_time,
            original_spread
        )
        
    # PART 2: If a pick does not exist in the session state, iterate through existing picks (max 3 iterations)
    else:
        # For each existing pick in the session state, check if the game ID matches the current game ID
        # If it does, update the existing pick with the new value
        # If it doesn't, add a new entry to the session state
        for existing_pick in st.session_state.point_picks:
            existing_game_id = existing_pick['game_id']
            same_id = False
            # if the game ID already exists in our list, update the same_id flag
            if existing_game_id == game_id:
                same_id = True
                # check if the key type is points or spread and update the appropriate value in the session state
                if key_type == "points":
                    existing_pick['point_value'] = value_of_pick
                elif key_type == "spread":
                    existing_pick['spread_pick'] = value_of_pick
                    # update is_pick_home for easier spread coverage calculation in view_player_picks.py
                    existing_pick['is_pick_home'] = is_pick_home
    
           # PART 3: Point conflict check (skips if the game ID is the same or if the value of the pick is None)
           # If the user selects a point value that has already been selected for a different game:
           # 1. Pop the old pick from the session state list
           # 2. Reset the button states for the old pick to None (deselects the button on the frontend)
            if not same_id and value_of_pick is not None:
                if key_type == "points" and value_of_pick == existing_pick['point_value']:
                    # print("different games with the same point value assignment - pop the old pick from the list")
                    st.toast(f"Resetting previous {existing_pick['point_value']} point pick, please do not make any new selections until this disappears!", icon="⏳", duration=4)

                    # pop the entire pick from the list if there was no spread value selected
                    # only append picks to the new session state list if that pick's point value is not equal to the selected point value
                    st.session_state.point_picks = [existing_pick for existing_pick in st.session_state.point_picks if existing_pick["point_value"] != value_of_pick]
                    # Recraft the original key so that it can be updated in the original session state that the buttons control
                    # i.e. 1_points or 1_spread
                    # Reset session state to None - deselects the button on the page
                    recrafted_key = str(existing_pick['button_id']) + "_points"
                    recrafted_key2 = str(existing_pick['button_id']) + "_spread"
                    st.session_state[recrafted_key2] = None
                    st.session_state[recrafted_key] = None
                    
        # if there is no duplicate, append it to the running list of picks
        if not same_id:
            add_new_pick_to_session_state(
                home_team_name, 
                away_team_name,
                value_of_pick if key_type == "points" else None, 
                value_of_pick if key_type == "spread" else None,
                is_pick_home,
                game_id,
                button_id,
                start_time,
                original_spread
            )
    
    # # print for debugging purposes
    # print("\n\n -------NEW ENTRY-------")
    # print(json.dumps(st.session_state.point_picks, indent=2))

# Creats a new dictionary entry in session state for each pick made by the user
def add_new_pick_to_session_state(home_team_name, away_team_name, point_value, spread_pick, is_pick_home, game_id, button_id, start_time, original_spread):
    st.session_state.point_picks.append({
        "home_team": home_team_name,
        "away_team": away_team_name,
        "point_value": point_value,
        "home_team_score": 0,
        "away_team_score": 0,
        "original_spread": original_spread,
        "spread_pick": spread_pick,
        "game_id": game_id,
        "is_pick_home": is_pick_home,
        "button_id": button_id,
        "is_pick_in_database": False,
        "start_time": start_time
    })

# Creates a new dictionary entry for each game that is displayed by the API call
# Can be queried by using (button_id - 1) - gets the proper list index
def add_new_game_information_to_session_state(button_id, game_id, home_team_name, away_team_name, spread, team_favored, start_time):
    st.session_state.game_information.append({
        "button_id": button_id,
        "game_id": game_id,
        "home_team": home_team_name,
        "away_team": away_team_name,
        "spread": spread,
        "team_favored": team_favored,
        "start_time": start_time,
    })

# Update button states based on the picks the user already made in the session state
# This is to avoid buttons being reset when the user navigates to a different page
def buttons_already_selected():
    for pick in st.session_state.point_picks:
        recrafted_key_points = str(pick['button_id']) + "_points"
        recrafted_key_spread = str(pick['button_id']) + "_spread"
        st.session_state[recrafted_key_points] = pick['point_value']
        st.session_state[recrafted_key_spread] = pick['spread_pick']