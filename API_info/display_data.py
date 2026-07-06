import streamlit as st
from css.streamlit_css import load_css_gamedisplay, load_css_buttons_gamepage
from API_info.abbreviation_mapping import map_abbreviations
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
    # store the abbreviation mapping in a variable for later use when displaying the data
    abbreviation_mapping = map_abbreviations()

    # sort the data by the commence_time key in ascending order so that the earliest games are displayed first
    data = sorted(data, key=lambda game: datetime.strptime(game['commence_time'], '%Y-%m-%dT%H:%M:%SZ'))

    st.markdown("### LISTING OF UPCOMING NFL GAMES AND THEIR POINT SPREADS", text_alignment="center")
    for data_obj in data[0:16]:
        # skip an iteration if no bookmaker is listed for the game
        if len(data_obj["bookmakers"]) == 0:
            continue
        else:
            load_css_buttons_gamepage()
            generate_expander(data_obj, button_id)
            button_id += 1

# Generate expander elements for each game made available from the API call
def generate_expander(data_obj, button_id):
    # extract home team, away team, point spreads for the favored and underdog teams, and the game ID from the API call data
    abbreviation_mapping = map_abbreviations()
    home_team = data_obj["home_team"]
    away_team = data_obj["away_team"]
    point_spread = data_obj["bookmakers"][0]["markets"][0]["outcomes"]
    team_favored, team_favored_abbreviation, point_spread_favored, team_underdog, team_underdog_abbreviation, point_spread_underdog = None, None, None, None, None, None
    is_spread_even = False

    # iterate through the point_spread list to find the favored and underdog teams and their respective point spreads
    for spread in point_spread:
        if spread["point"] == 0:
            is_spread_even = True
            break
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
        team_favored = f"EVEN"
        point_spread_favored = ''
        team_underdog = f"EVEN"
        point_spread_underdog = ''
    
    game_id = data_obj['id']

    # # convert date_time into a datetime object
    # # convert to EST
    # Not using this yet so comment it out
    # date_time = datetime.strptime(data_obj['commence_time'], '%Y-%m-%dT%H:%M:%SZ')
    # date_time = date_time.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/New_York"))

    # create a new entry in the session state for the game
    add_new_game_information_to_session_state(button_id, game_id, home_team, away_team, point_spread, team_favored)

    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        with st.expander(f'''{away_team} @ {home_team} → → → → Spread: {team_favored_abbreviation} {point_spread_favored}''', expanded=False):
            # create columns within the expander to display team logs
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.image(f"images_nfl/{away_team.lower()}.png", width=100)
                
            with col2:
                # make the @ symbol larger and centered between the team logos
                st.markdown(
                f'''<div 
                        style='text-align: center; 
                        font-size: 6rem;'>
                        @
                    </div>
                ''', unsafe_allow_html=True)    
            with col3:
                st.image(f"images_nfl/{home_team.lower()}.png", width=100)
            
            # display the date and time of the game in a readable format
            # display the over/under line for the game
            st.markdown(f"## **SPREAD**: {team_favored_abbreviation} {point_spread_favored}", text_alignment='center')
            
            # Create columns with an intentionally narrow middle column
            # center the segmented controls in the middle column
            # segmented control allows the user to make selections, and the key is stored in session state for tracking
            # on_change contains a reference to a callback function, args passes in the changed key upon change
            # allows us to edit states manually when the user clicks on buttons on the frontend
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.segmented_control (
                    label="spread", 
                    options=[f"{team_favored_abbreviation} {point_spread_favored}", f"{team_underdog_abbreviation} +{point_spread_underdog}"], 
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
def handle_change(changed_key, game_info):
    duplicate_exists = False
    # Split the changed key to get key type ("points" or "spread")
    key_type = changed_key.split("_")[1]
    button_id = int(changed_key.split("_")[0])

    # get the game information for the button that was clicked
    game = game_info[button_id - 1]
    home_team_name = game["home_team"]
    away_team_name = game["away_team"]
    game_id = game["game_id"]
    
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
    
            # If the point selection conflicts with another point selection, pop the old selection from the list
            # Does not check for a conflict if the game ID is the same (i.e. the user is changing their pick for the same game)
            if key_type == "points":
                if st.session_state[changed_key] == pick['point_value'] and not same_id:
                    # print("different games with the same point value assignment - pop the old pick from the list")
                    st.toast(f"Resetting previous {pick['point_value']} point pick, please do not make any new selections until this disappears!", icon="⏳", duration=2)

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
            game_id,
            button_id
        )
        
    # print for debugging
    print("\n\n -------NEW ENTRY-------")
    print(json.dumps(st.session_state.point_picks, indent=2))

# Creats a new dictionary entry in session state for each pick made by the user
def add_new_pick_to_session_state(home_team_name, away_team_name, point_value, spread_pick, game_id, button_id):
    st.session_state.point_picks.append({
        "home_team": home_team_name,
        "away_team": away_team_name,
        "point_value": point_value,
        "spread": spread_pick,
        "game_id": game_id,
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
        "team_favored": team_favored
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