import streamlit as st
from css.streamlit_css import load_css_gamedisplay
from API_info.abbreviation_mapping import map_abbreviations, reverse_map_abbreviations
import json
from datetime import datetime
from zoneinfo import ZoneInfo


# Display the upcoming NFL games and point spreads
def display_data_nfl (data):
    button_id = 1
    # create the game_information list in session state if it doesn't already exist
    if "game_information" not in st.session_state:
        st.session_state.game_information = []
    
    # reset session state for game information if it already exists
    # clicking on buttons rerenders the entire page, which would cause this list to grow indefinitely
    if "game_information" in st.session_state:
        st.session_state.game_information = []

    # load hacky CSS that messes with the expander element display
    load_css_gamedisplay()
    # checks if the user has already made picks in this session - updates state accordingly
    buttons_already_selected()

    st.markdown("### LISTING OF UPCOMING NFL GAMES AND THEIR POINT SPREADS", text_alignment="center")
    start_times_list = []
    for data_obj in data[0:16]:
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
    abbreviation_mapping = map_abbreviations()
    home_team = data_obj["home_team"]
    away_team = data_obj["away_team"]
    start_time = data_obj["commence_time"]
    point_spread = data_obj["bookmakers"][0]["markets"][0]["outcomes"]
    team_favored, team_favored_abbreviation, point_spread_favored, team_underdog, team_underdog_abbreviation, point_spread_underdog = None, None, None, None, None, None
    is_spread_even = False

    # iterate through the point_spread list to find the favored and underdog teams and their respective point spreads
    for spread in point_spread:
        if spread["point"] == 0:
            is_spread_even = True
        if spread["point"] < 0:
            team_favored = spread["name"]
            team_favored_abbreviation = abbreviation_mapping[team_favored]
            point_spread_favored = spread["point"]
        if spread["point"] > 0:
            team_underdog = spread["name"]
            team_underdog_abbreviation = abbreviation_mapping[team_underdog]
            point_spread_underdog = spread["point"]

    # If the spread is 0, that means the spread is even
    # In that case, we will set the favored and underdog teams to "EVEN" and the point spreads to empty strings
    if is_spread_even:
        home_team_abbreviation = abbreviation_mapping[home_team]
        away_team_abbreviation = abbreviation_mapping[away_team]
    
    game_id = data_obj['id']

    # create a new entry in the session state for the game
    add_new_game_information_to_session_state(button_id, game_id, home_team, away_team, point_spread, team_favored)

    # First, check if the list is empty. If it is, append an entry and display it to the page
    if len(start_times_list) == 0:
        st.divider(width='stretch')
        start_times_list.append(start_time)
        # create a datetime object from start time, replace its info with UTC, convert it to EST, and then format it in a readable string
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/New_York")).strftime('%A, %B %d at %I:%M %p EST')
        st.markdown(f"### :red[{start_time}]", text_alignment='center')
    # If it's not empty, iterate through the list to see if a duplicate entry exists. If it does, break the loop and do not display it to the page
    else:
        for previous_start_times in start_times_list:
            if start_time == previous_start_times:
                break
        
        # If it doesn't exist, append it to the list and display it to the page
        else:
            st.divider(width='stretch')
            start_times_list.append(start_time)
            # create a datetime object from start time, replace its info with UTC, convert it to EST, and then format it in a readable string
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/New_York")).strftime('%A, %B %d at %I:%M %p EST')
            st.markdown(f"### :red[{start_time}]", text_alignment='center')

    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        if is_spread_even:
            expander_string = f"{away_team} @ {home_team} → → → → Spread: EVEN"
        else:
            expander_string = f"{away_team} @ {home_team} → → → → Spread: {team_favored_abbreviation} {point_spread_favored}"
        with st.expander(expander_string, expanded=False):
            # create columns within the expander to display team logs
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.image(f"images_nfl/{away_team.lower()}.png", width=100)
                
            with col2:  
                st.title(f"@", text_alignment='center') 
            with col3:
                st.image(f"images_nfl/{home_team.lower()}.png", width=100)
            
            # display the date and time of the game in a readable format
            # display the over/under line for the game
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
                button_id += 1
                st.divider(width='stretch')

# Callback function that handles changes to point values and updates states accordingly
# TODO: this function is quite the struggle to parse through - it will be refactored after the completion of MVP #5
def handle_change(changed_key, game_info):
    duplicate_exists = False
    # Split the changed key to get key type ("points" or "spread")
    key_type = changed_key.split("_")[1]
    button_id = int(changed_key.split("_")[0])
    print(f"CHANGED KEY: {changed_key} | KEY TYPE: {key_type} | BUTTON ID: {button_id}")

    # get the game information for the button that was clicked
    reverse_abbreviation_mapping = reverse_map_abbreviations()
    game = game_info[button_id - 1]
    home_team_name = game["home_team"]
    away_team_name = game["away_team"]
    game_id = game["game_id"]
    is_pick_home = False

    # If the key type is spread, determine if the pick is for the home team or the away team
    # This helps later when we are calculating if the pick covered the spread or not
    if key_type == "spread":
        spread_pick = st.session_state[changed_key]
        pick_abbreviation = spread_pick.split(" ")[0]
        print(reverse_abbreviation_mapping[pick_abbreviation])
        print(home_team_name)
        if reverse_abbreviation_mapping[pick_abbreviation] == home_team_name:
            is_pick_home = True
    
    # If there are picks currently listed in the session state
    if st.session_state.point_picks:
        # print("picks do exist in list")
        # check if the game ID already exists in the point_picks list
        for pick in st.session_state.point_picks:
            # print(f"for {pick} in the full list")
            # get the game ID for the current pick selected in the loop
            current_game_id = pick['game_id']
            same_id = False
            # if the game ID already exists in our list, update the point value and the flag that tracks duplicates
            # print (f"{current_game_id} ------ {game_id}")
            if current_game_id == game_id:
                same_id = True
                duplicate_exists = True
                
                # check if the key type is points or spread and update the appropriate value in the session state
                if key_type == "points":
                    # print("updating point value!")
                    pick['point_value'] = st.session_state[changed_key]
                elif key_type == "spread":
                    # print("updating spread value!")
                    pick['spread'] = st.session_state[changed_key]
                    pick['is_pick_home'] = is_pick_home
    
            # If the point selection conflicts with another point selection, pop the old selection from the list
            # Does not check for a conflict if the game ID is the same (i.e. the user is changing their pick for the same game)
            if key_type == "points":
                if st.session_state[changed_key] == pick['point_value'] and not same_id:
                    # print("different games with the same point value assignment - pop the old pick from the list")
                    st.toast(f"Resetting previous {pick['point_value']} point pick, please do not make any new selections until this disappears!", icon="⏳", duration=4)

                    # pop the entire pick from the list if there was no spread value selected
                    # only append picks to the new session state list if that pick's point value is not equal to the selected point value
                    st.session_state.point_picks = [existing_pick for existing_pick in st.session_state.point_picks if existing_pick["point_value"] != st.session_state[changed_key]]
                    # Recraft the original key so that it can be updated in the original session state that the buttons control
                    # i.e. 1_points or 1_spread
                    # Reset session state to None - deselects the button on the page
                    recrafted_key = str(pick['button_id']) + "_points"
                    recrafted_key2 = str(pick['button_id']) + "_spread"
                    st.session_state[recrafted_key2] = None
                    st.session_state[recrafted_key] = None
                
        # if there is no duplicate, append it to the running list of picks
        if not duplicate_exists:
            # print("no duplicate exists - adding new value")
            add_new_pick_to_session_state(
                home_team_name, 
                away_team_name,
                st.session_state[changed_key] if key_type == "points" else None, 
                st.session_state[changed_key] if key_type == "spread" else None,
                is_pick_home,
                game_id,
                button_id
            )
    
    # otherwise, if there are no picks in the session state, append a new entry to the session state
    else:
        # print("picks do not exist yet - add a new entry!")
        add_new_pick_to_session_state(
            home_team_name, 
            away_team_name,
            st.session_state[changed_key] if key_type == "points" else None, 
            st.session_state[changed_key] if key_type == "spread" else None,
            is_pick_home,
            game_id,
            button_id
        )
        
    # print for debugging
    print("\n\n -------NEW ENTRY-------")
    print(json.dumps(st.session_state.point_picks, indent=2))

# Creats a new dictionary entry in session state for each pick made by the user
def add_new_pick_to_session_state(home_team_name, away_team_name, point_value, spread_pick, is_pick_home, game_id, button_id):
    st.session_state.point_picks.append({
        "home_team": home_team_name,
        "away_team": away_team_name,
        "point_value": point_value,
        "spread": spread_pick,
        "game_id": game_id,
        "is_pick_home": is_pick_home,
        "button_id": button_id
    })

# Creates a new dictionary entry for each game in the API call to narrow down relevant information for later usage
def add_new_game_information_to_session_state(button_id, game_id, home_team_name, away_team_name, spread, team_favored):
    st.session_state.game_information.append({
        "button_id": button_id,
        "game_id": game_id,
        "home_team": home_team_name,
        "away_team": away_team_name,
        "spread": spread,
        "team_favored": team_favored,
    })

# Update button states based on the picks the user already made in the session state
# This is to avoid buttons being reset when the user navigates to a different page
def buttons_already_selected():
    for pick in st.session_state.point_picks:
        recrafted_key_points = str(pick['button_id']) + "_points"
        recrafted_key_spread = str(pick['button_id']) + "_spread"
        st.session_state[recrafted_key_points] = pick['point_value']
        st.session_state[recrafted_key_spread] = pick['spread']

# For later when we're gonna go week by week for the NFL
def calculate_date_time():
    pass