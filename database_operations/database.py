# Module that handles all database operations across the application
# Makes it easier to track where DB interactions happen throughout the program

from st_supabase_connection import SupabaseConnection
import streamlit as st

def get_all_user_picks():
    conn = st.connection("user_picks", type=SupabaseConnection)
    rows = conn.table("user_picks").select("*").execute().data
    return rows

def create_user_db_entry(data_entry):
    conn = st.connection("user_picks", type=SupabaseConnection)
    conn.table("user_picks").insert(data_entry).execute()

def update_user_picks(name, data_entry):
    conn = st.connection("user_picks", type=SupabaseConnection)
    conn.table("user_picks").update(data_entry).eq("name", name).execute()
    
def update_user_points(name, current_week_total, accumulated_points):
    conn = st.connection("user_picks", type=SupabaseConnection)
    conn.table("user_picks").update({
            "current_week_total": current_week_total, 
            "accumulated_points": accumulated_points
        }).eq("name", name).execute()

def get_user_points():
    name_list = ["Dad", "TJ", "Tyler"]
    conn = st.connection("user_picks", type=SupabaseConnection)
    for name in name_list:
        row = conn.table("user_picks").select("accumulated_points").eq("name", name).execute().data
        if row:
            accumulated_points = row[0]["accumulated_points"]
            st.session_state[f"{name}_accumulated_points"] = accumulated_points
            print(st.session_state[f"{name}_accumulated_points"])