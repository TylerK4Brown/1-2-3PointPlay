import streamlit as st
from css.streamlit_css import load_css_gamedisplay
import json
from datetime import datetime
from zoneinfo import ZoneInfo

# Display the upcoming MLB games and O/U numbers
def display_data_mlb (data):
    over_under = None
    button_id = 1
    if "game_information" not in st.session_state:
        st.session_state.game_information = []
    # load hacky CSS that messes with the expander element display
    load_css_gamedisplay()
    # checks if the user has already made picks in this session - updates state accordingly
    buttons_already_selected()

    # sort the data by the commence_time key in ascending order so that the earliest games are displayed first
    data = sorted(data, key=lambda game: datetime.strptime(game['commence_time'], '%Y-%m-%dT%H:%M:%SZ'))

    st.markdown("### LISTING OF UPCOMING MLB GAMES AND THEIR OVER/UNDERS", text_alignment="center")

    # TODO: store gameID in session state on this loop to avoid having to loop through the data again when the user selects something
    for data_obj in data[0:16]:
        # skip an iteration if no bookmaker is listed for the game
        if len(data_obj["bookmakers"]) == 0:
            continue
        else:
            # create multiple expanders for each game
            # home and away team names displayed, plus the over/under number for the game
            home_team = data_obj["home_team"]
            away_team = data_obj["away_team"]
            over_under = data_obj["bookmakers"][0]["markets"][0]["outcomes"][0]["point"]
            game_id = data_obj['id']

            # convert date_time into a datetime object
            # convert to EST
            date_time = datetime.strptime(data_obj['commence_time'], '%Y-%m-%dT%H:%M:%SZ')
            date_time = date_time.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/New_York"))

            add_new_game_information_to_session_state(button_id, game_id, home_team, away_team, over_under)

            col1, col2, col3 = st.columns([1, 5, 1])
            with col2:
                with st.expander(f'''{away_team} @ {home_team}, O/U: {over_under}''', expanded=False):
                    # create columns within the expander to display team logs
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        st.image(f"images/{away_team.lower()}.png", width=200, caption=f"{away_team}")
                        
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
                        st.image(f"images/{home_team.lower()}.png", width=200, caption=f"{home_team}")
                    
                    # display the date and time of the game in a readable format
                    # display the over/under line for the game
                    st.markdown(f"## **O/U**: {over_under}", text_alignment='center')
                    
                    # Create columns with an intentionally narrow middle column
                    # center the segmented controls in the middle column
                    # segmented control allows the user to make selections, and the key is stored in session state for tracking
                    # on_change contains a reference to a callback function, args passes in the changed key upon change
                    # allows us to edit states manually when the user clicks on buttons on the frontend
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.segmented_control (
                            label="over_under", 
                            options=["OVER", "UNDER"], 
                            key=f"{button_id}_OU", 
                            width="stretch", 
                            label_visibility="collapsed",
                            on_change=handle_change,
                            args=(f"{button_id}_OU", st.session_state.game_information,)
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
    # Split the changed key to get key type ("points" or "OU") and the home team name
    key_type = changed_key.split("_")[1]
    button_id = int(changed_key.split("_")[0])

    # get the game information for the button that was clicked
    game = game_info[button_id - 1]
    home_team_name = game["home_team"]
    away_team_name = game["away_team"]
    over_under_score = game["over_under_score"]
    game_id = game["game_id"]
    
    # If there are picks currently listed in the session state
    if st.session_state.point_picks:
        print("picks do exist in list")
        # check if the game ID already exists in the point_picks list
        for pick in st.session_state.point_picks:
            print(f"for {pick} in the full list")
            # get the game ID for the current pick selected in the loop
            current_game_id = pick['game_id']
            same_ID = False
            # if the game ID already exists in our list, update the point value and the flag that tracks duplicates
            print (f"{current_game_id} ------ {game_id}")
            if current_game_id == game_id:
                same_ID = True
                duplicate_exists = True
                
                # check if the key type is points or OU and update the appropriate value in the session state
                if key_type == "points":
                    print("updating point value!")
                    pick['point_value'] = st.session_state[changed_key]
                elif key_type == "OU":
                    print("updating OU value!")
                    pick['over_under'] = st.session_state[changed_key]
            
            # If the point selection conflicts with another point selection, pop the old selection from the list
            # Does not check for a conflict if the game ID is the same (i.e. the user is changing their pick for the same game)
            if key_type == "points":
                if st.session_state[changed_key] == pick['point_value'] and not same_ID:
                    print("different games with the same point value assignment - pop the old pick from the list")

                    # pop the entire pick from the list if there was no over/under value selected
                    # only append picks to the new session state list if that pick's point value is not equal to the selected point value
                    st.session_state.point_picks = [pick for pick in st.session_state.point_picks if pick["point_value"] != st.session_state[changed_key]]
                    # Recraft the original key so that it can be updated in the original session state that the buttons control
                    # i.e. "Arizona Diamondbacks" now goes to "Arizona Diamondbacks_points"
                    # Reset session state to None - deselects the button on the page
                    recrafted_key = str(pick['button_id']) + "_points"
                    recrafted_key2 = str(pick['button_id']) + "_OU"
                    st.session_state[recrafted_key2] = None
                    st.session_state[recrafted_key] = None

        # if there is no duplicate, append it to the running list of picks
        if not duplicate_exists:
            print("no duplicate exists - adding new value")
            add_new_pick_to_session_state(
                home_team_name, 
                away_team_name,
                st.session_state[changed_key] if key_type == "points" else None, 
                st.session_state[changed_key] if key_type == "OU" else None, 
                over_under_score,
                game_id,
                button_id
            )
    
    # otherwise, if there are no picks in the session state, append a new entry to the session state
    else:
        print("picks do not exist yet - add a new entry!")
        add_new_pick_to_session_state(
            home_team_name, 
            away_team_name,
            st.session_state[changed_key] if key_type == "points" else None, 
            st.session_state[changed_key] if key_type == "OU" else None,
            over_under_score,
            game_id,
            button_id
        )
        
    # print for debugging
    print(json.dumps(st.session_state.point_picks, indent=2))

def add_new_pick_to_session_state(home_team_name, away_team_name, point_value, over_under, over_under_score, game_id, button_id):
    st.session_state.point_picks.append({
        "home_team": home_team_name,
        "away_team": away_team_name,
        "point_value": point_value,
        "over_under": over_under,
        "over_under_score": over_under_score,
        "game_id": game_id,
        "button_id": button_id
    })

def add_new_game_information_to_session_state(button_id, game_id, home_team_name, away_team_name, over_under_score):
    st.session_state.game_information.append({
        "button_id": button_id,
        "game_id": game_id,
        "home_team": home_team_name,
        "away_team": away_team_name,
        "over_under_score": over_under_score
    })

# For later when we're gonna go week by week for the NFL
def calculate_date_time():
    pass

# Update button states based on the picks the user already made in the session state
def buttons_already_selected():
    for pick in st.session_state.point_picks:
        recrafted_key_points = str(pick['button_id']) + "_points"
        recrafted_key_OU = str(pick['button_id']) + "_OU"
        st.session_state[recrafted_key_points] = pick['point_value']
        st.session_state[recrafted_key_OU] = pick['over_under']