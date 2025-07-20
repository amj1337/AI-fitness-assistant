import requests
import streamlit as st

def get_user_context(user_id):
    """Fetch user context from backend"""
    try:
        response = requests.get(
            f"http://localhost:8000/users/{user_id}",
            timeout=2
        )
        if response.status_code == 200:
            user_data = response.json()
            
            # Get latest progress
            progress_response = requests.get(
                f"http://localhost:8000/progress?user_id={user_id}&limit=1"
            )
            progress_data = progress_response.json()
            
            return {
                "name": user_data.get("name", ""),
                "email": user_data.get("email", ""),
                "goals": user_data.get("goals", "Not set"),
                "preferences": user_data.get("preferences", "Not set"),
                "last_progress": format_progress(progress_data[0]) if progress_data else "No data"
            }
    except:
        pass
    return {}

def format_progress(progress):
    """Format progress data for display"""
    if not progress:
        return "No data"
    return f"{progress.get('weight', '?')}kg, {progress.get('body_fat', '?')}% BF"

def format_date(date_str):
    """Format date string for display"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
    except:
        return date_str

def display_chat_message(speaker, message):
    """Display a chat message with appropriate styling"""
    if speaker == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(message)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(message)