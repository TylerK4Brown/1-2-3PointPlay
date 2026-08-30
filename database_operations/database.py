# database.py
# All database interactions are handled in this file, assisting with many repetitive database operations throughout the application
# Separating this file out into one module allows for easier maintenance and debugging of database operations

from st_supabase_connection import SupabaseConnection
import streamlit as st

DB_NAME = "user_picks_preseason_1"

# ======== CREATE OPERATIONS ==========
# Create a new user entry in the database if the name does not exist yet
# This will only be used at the start of the season to create initial entries for each user
def create_user_db_entry(data_entry):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    conn.table(DB_NAME).insert(data_entry).execute()

# ======== GET OPERATIONS ==========
# Get all user picks
# Select * from the dev_picks table and return the rows
def get_all_user_picks():
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    rows = conn.table(DB_NAME).select("*").execute().data
    return rows

# Get the picks for one single user
def get_user_picks(name):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    row = conn.table(DB_NAME).select("*").eq("name", name).execute().data
    return row

# Get the picks from a specific week for a specific user
# Used to find historical picks for a specific week
def get_picks_by_week(week_number, name):
    week = f"week_{week_number}"
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    if name is None:
        rows = conn.table(DB_NAME).select(week).execute().data
    else:
        rows = conn.table(DB_NAME).select(week).eq("name", name).execute().data
    return rows

# Get the player's total points for a specific week from the database
def get_point_total_for_week(week_number, name):
    point_total_col_name = f"point_total_week_{week_number}"
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    row = conn.table(DB_NAME).select(point_total_col_name).eq("name", name).execute().data
    point_total = row[0][point_total_col_name]
    return point_total

# Get the player's win/loss record for a specific week from the database
# Used in the pick history page to display the player's win/loss record from each week
def get_win_loss_by_week(week_number, name):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    row = conn.table(DB_NAME).select(f"win_loss_week_{week_number}").eq("name", name).execute().data
    win_loss = row[0][f"win_loss_week_{week_number}"]
    return win_loss

# Get the player's current win/loss record from the database
def get_win_loss_record(name):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    row = conn.table(DB_NAME).select("win_loss_record").eq("name", name).execute().data
    win_loss_record = row[0]["win_loss_record"]
    return win_loss_record

def update_win_loss_info(name, correct_picks, incorrect_picks, push_picks):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    win_loss_json = {
        "picks_correct": correct_picks,
        "picks_incorrect": incorrect_picks,
        "picks_push": push_picks
    }
    conn.table(DB_NAME).update({"win_loss_record": win_loss_json}).eq("name", name).execute()

def get_win_loss_by_week(week_number, name):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    row = conn.table(DB_NAME).select(f"win_loss_week_{week_number}").eq("name", name).execute().data
    win_loss = row[0][f"win_loss_week_{week_number}"]
    return win_loss

def get_win_loss_record(name):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    row = conn.table(DB_NAME).select("win_loss_record").eq("name", name).execute().data
    win_loss_record = row[0]["win_loss_record"]
    return win_loss_record

# Get the current user points for each user, store in session state
# Used in the leaderboard page to display accumulated points for each user
def get_user_points():
    name_list = ["Dad", "TJ", "Tyler"]
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    for name in name_list:
        row = conn.table(DB_NAME).select("accumulated_points").eq("name", name).execute().data
        if row:
            accumulated_points = row[0]["accumulated_points"]
            st.session_state[f"{name}_accumulated_points"] = accumulated_points

# Get the current week number from the database
def get_week_number():
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    row = conn.table(DB_NAME).select("current_week").eq("name", "Tyler").execute().data
    current_week_number = row[0]["current_week"]
    return current_week_number

# ======== UPDATE OPERATIONS ==========
# Update the picks in the database for a specific user
def update_user_picks(name, data_entry):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    conn.table(DB_NAME).update(data_entry).eq("name", name).execute()

# Update points for a specific user in the database
# Called after user clicks on the "view_player_picks" page
# Updates point totals based on the live score of the game
# Also updates the home and away team score for that game
def update_user_points(name, current_week_total, accumulated_points):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    conn.table(DB_NAME).update({
            "current_week_total": current_week_total, 
            "accumulated_points": accumulated_points
        }).eq("name", name).execute()

# Update win/loss information after loading the "view_player_picks" page
# Stores any differences that may have occurred in the win/loss record for the current week in the database
def update_win_loss_info(name, correct_picks, incorrect_picks, push_picks):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    win_loss_json = {
        "picks_correct": correct_picks,
        "picks_incorrect": incorrect_picks,
        "picks_push": push_picks
    }
    conn.table(DB_NAME).update({"win_loss_record": win_loss_json}).eq("name", name).execute()

# Update the score of a specific pick for a specific user in the database
# Called after clicking on the "view_player_picks" page, after the API call is made to get the live scores for each game
def update_scores(name, score_home_team, score_away_team, iteration_index, sorted_picks, covering_spread):
    conn = st.connection(DB_NAME, type=SupabaseConnection)
    # update the pick at the specific index (0 - 2)
    pick_to_update = sorted_picks[iteration_index]
    # update the home team/away team scores + the covering status
    pick_to_update["home_team_score"] = score_home_team
    pick_to_update["away_team_score"] = score_away_team
    pick_to_update["covering_spread"] = covering_spread
    # update the picks in the DB
    conn.table(DB_NAME).update({
            "current_picks": {
                "picks": sorted_picks
            }
        }).eq("name", name).execute()