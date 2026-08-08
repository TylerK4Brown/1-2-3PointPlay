# Module that handles all database operations across the application
# Makes it easier to track where DB interactions happen throughout the program

from st_supabase_connection import SupabaseConnection
import streamlit as st

# Get all user picks
# Select * from the user_picks table and return the rows
def get_all_user_picks():
    conn = st.connection("user_picks", type=SupabaseConnection)
    rows = conn.table("user_picks").select("*").execute().data
    return rows

# Get the picks for one single user
def get_user_picks(name):
    conn = st.connection("user_picks", type=SupabaseConnection)
    row = conn.table("user_picks").select("*").eq("name", name).execute().data
    return row

# Create a new user entry in the database if the name does not exist yet
# This will only be used at the start of the season to create initial entries for each user
def create_user_db_entry(data_entry):
    conn = st.connection("user_picks", type=SupabaseConnection)
    conn.table("user_picks").insert(data_entry).execute()

def get_picks_by_week(week_number, name):
    week = f"week_{week_number}"
    conn = st.connection("user_picks", type=SupabaseConnection)
    if name is None:
        rows = conn.table("user_picks").select(week).execute().data
    else:
        rows = conn.table("user_picks").select(week).eq("name", name).execute().data
    return rows

# Get the player's total points for a specific week from the database
def get_point_total_for_week(week_number, name):
    point_total_col_name = f"point_total_week_{week_number}"
    conn = st.connection("user_picks", type=SupabaseConnection)
    row = conn.table("user_picks").select(point_total_col_name).eq("name", name).execute().data
    point_total = row[0][point_total_col_name]
    return point_total

# Update the user picks in the database for a specific user
def update_user_picks(name, data_entry):
    conn = st.connection("user_picks", type=SupabaseConnection)
    conn.table("user_picks").update(data_entry).eq("name", name).execute()

# Update points for a specific user in the database
# Called after user clicks on the "view_player_picks" page
# Updates point totals based on the live score of the game
# Also updates the home and away team score for that game, plus the covering status
def update_user_points(name, current_week_total, accumulated_points):
    conn = st.connection("user_picks", type=SupabaseConnection)
    conn.table("user_picks").update({
            "current_week_total": current_week_total, 
            "accumulated_points": accumulated_points
        }).eq("name", name).execute()

# Get the current user points for each user, store in session state
# Used in the leaderboard page to display accumulated points for each user
def get_user_points():
    name_list = ["Dad", "TJ", "Tyler"]
    conn = st.connection("user_picks", type=SupabaseConnection)
    for name in name_list:
        row = conn.table("user_picks").select("accumulated_points").eq("name", name).execute().data
        if row:
            accumulated_points = row[0]["accumulated_points"]
            st.session_state[f"{name}_accumulated_points"] = accumulated_points

# Update the score of a specific pick for a specific user in the database
# Called after clicking on the "view_player_picks" page, after the API call is made to get the live scores for each game
def update_scores(name, score_home_team, score_away_team, iteration_index, sorted_picks, covering_spread):
    conn = st.connection("user_picks", type=SupabaseConnection)
    # update the pick at the specific index (0 - 2)
    pick_to_update = sorted_picks[iteration_index]
    # update the home team/away team scores + the covering status
    pick_to_update["home_team_score"] = score_home_team
    pick_to_update["away_team_score"] = score_away_team
    pick_to_update["covering_spread"] = covering_spread
    # update the picks in the DB
    conn.table("user_picks").update({
            "current_picks": {
                "picks": sorted_picks
            }
        }).eq("name", name).execute()

# Get the current week number from the database
def get_week_number():
    conn = st.connection("user_picks", type=SupabaseConnection)
    row = conn.table("user_picks").select("current_week").eq("name", "Tyler").execute().data
    current_week_number = row[0]["current_week"]
    return current_week_number