import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from utls import get_user_context, format_date, display_chat_message
import time

# Page configuration
st.set_page_config(
    page_title="Your Personal Fitness Assistant",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "user_id" not in st.session_state:
        st.session_state.user_id = 1  # Default user for demo
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Chat with Assistant"
    if "last_response" not in st.session_state:
        st.session_state.last_response = None
    if "user_context" not in st.session_state:
        st.session_state.user_context = get_user_context(st.session_state.user_id)

# Initialize session
init_session_state()

# Sidebar navigation
with st.sidebar:
    #st.image("https://i.imgur.com/XYZ1234.png", width=150)  # Add your logo URL
    #st.title("FitGPT Navigation")
    
    # User selection
    st.session_state.user_id = st.selectbox(
        "Select User", 
        options=[1, 2, 3],  # Replace with actual user IDs from your DB
        index=0,
        key="user_selector"
    )
    
    # Navigation
    st.session_state.current_page = st.radio(
        "Menu",
        options=["Chat with Assistant", "Log Workout", "Log Diet", "View Progress"],
        index=["Chat with Assistant", "Log Workout", "Log Diet", "View Progress"].index(st.session_state.current_page)
    )
    
    # Update context when user changes
    if st.button("Refresh User Data"):
        st.session_state.user_context = get_user_context(st.session_state.user_id)
        st.success("User data refreshed!")
    
    # User context display
    st.subheader("Your Fitness Profile")
    st.markdown(f"**Goals:** {st.session_state.user_context.get('goals', 'Not set')}")
    st.markdown(f"**Preferences:** {st.session_state.user_context.get('preferences', 'Not set')}")
    st.markdown(f"**Last Progress:** {st.session_state.user_context.get('last_progress', 'No data')}")
    
    # System status
    st.divider()
    st.caption(f"API Status: {'🟢 Connected' if st.session_state.get('api_status', False) else '🔴 Disconnected'}")
    st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Main content area
st.title("💪 Your Personal Fitness Assistant")
st.caption("Your AI-powered personal trainer")

# Check API connection
try:
    response = requests.get("http://localhost:8000/health", timeout=2)
    st.session_state.api_status = response.status_code == 200
except:
    st.session_state.api_status = False

if not st.session_state.api_status:
    st.error("Backend API is not available. Please start the FastAPI server.")
    st.stop()

# Chat Interface
if st.session_state.current_page == "Chat with Assistant":
    st.subheader("Chat with Your Fitness Assistant")
    
    # Display conversation history
    chat_container = st.container(height=400)
    with chat_container:
        for speaker, message in st.session_state.conversation:
            display_chat_message(speaker, message)
    
    # Input area
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Your message:", 
                placeholder="Ask about workouts, nutrition, or progress...",
                label_visibility="collapsed"
            )
        with col2:
            submit_chat = st.form_submit_button("Send", use_container_width=True)
    
    if submit_chat and user_input:
        # Add user message to conversation
        st.session_state.conversation.append(("user", user_input))
        
        # Show typing indicator
        with chat_container:
            with st.status("Assistant is thinking...", expanded=False) as status:
                with st.empty():
                    # Send to backend
                    try:
                        response = requests.post(
                            "http://localhost:8000/chat",
                            json={
                                "user_id": st.session_state.user_id,
                                "message": user_input
                            }
                        ).json()
                        assistant_response = response["response"]
                    except Exception as e:
                        assistant_response = f"Error: {str(e)}"
                
                # Add assistant response
                st.session_state.conversation.append(("assistant", assistant_response))
                st.session_state.last_response = assistant_response
                status.update(label="Response ready", state="complete")
        
        # Rerun to update conversation display
        st.rerun()

# Log Workout Page
elif st.session_state.current_page == "Log Workout":
    st.subheader("Log Your Workout")
    
    with st.form("workout_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            workout_date = st.date_input("Date", value=date.today())
            workout_type = st.selectbox(
                "Workout Type", 
                options=["Cardio", "Strength Training", "HIIT", "Yoga", "Swimming", "Cycling"]
            )
        with col2:
            duration = st.slider("Duration (minutes)", 5, 180, 30)
            intensity = st.select_slider(
                "Intensity Level", 
                options=["Light", "Moderate", "Vigorous", "Max Effort"]
            )
        
        notes = st.text_area("Workout Notes", placeholder="Describe your workout...")
        
        submit_workout = st.form_submit_button("Save Workout", type="primary")
        
        if submit_workout:
            workout_data = {
                "user_id": st.session_state.user_id,
                "date": str(workout_date),
                "type": workout_type,
                "duration": duration,
                "intensity": intensity,
                "notes": notes
            }
            
            try:
                response = requests.post(
                    "http://localhost:8000/workouts",
                    json=workout_data
                )
                
                if response.status_code == 200:
                    st.success("Workout logged successfully!")
                    st.session_state.user_context = get_user_context(st.session_state.user_id)
                    time.sleep(1)
                    st.session_state.current_page = "View Progress"
                    st.rerun()
                else:
                    st.error(f"Error logging workout: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# Log Diet Page
elif st.session_state.current_page == "Log Diet":
    st.subheader("Log Your Meal")
    
    with st.form("diet_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            meal_date = st.date_input("Date", value=date.today())
            meal_type = st.selectbox(
                "Meal Type", 
                options=["Breakfast", "Lunch", "Dinner", "Snack"]
            )
        with col2:
            calories = st.number_input("Calories", min_value=0, max_value=2000, value=500)
            protein = st.number_input("Protein (g)", min_value=0, max_value=100, value=20)
            carbs = st.number_input("Carbs (g)", min_value=0, max_value=100, value=40)
            fat = st.number_input("Fat (g)", min_value=0, max_value=100, value=15)
        
        meal_description = st.text_area(
            "Meal Description", 
            placeholder="Describe your meal (e.g., Grilled chicken with vegetables)..."
        )
        
        submit_meal = st.form_submit_button("Save Meal", type="primary")
        
        if submit_meal:
            meal_data = {
                "user_id": st.session_state.user_id,
                "date": str(meal_date),
                "meal": meal_description,
                "calories": calories,
                "protein": protein,
                "carbs": carbs,
                "fat": fat,
                "meal_type": meal_type
            }
            
            try:
                response = requests.post(
                    "http://localhost:8000/diet",
                    json=meal_data
                )
                
                if response.status_code == 200:
                    st.success("Meal logged successfully!")
                    time.sleep(1)
                    st.session_state.current_page = "View Progress"
                    st.rerun()
                else:
                    st.error(f"Error logging meal: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# Progress Dashboard
elif st.session_state.current_page == "View Progress":
    st.subheader("Your Fitness Progress")
    
    try:
        # Fetch progress data
        progress_response = requests.get(
            f"http://localhost:8000/progress?user_id={st.session_state.user_id}"
        )
        progress_data = progress_response.json()
        
        # Fetch workout data
        workouts_response = requests.get(
            f"http://localhost:8000/workouts?user_id={st.session_state.user_id}"
        )
        workouts_data = workouts_response.json()
        
        # Fetch diet data
        diet_response = requests.get(
            f"http://localhost:8000/diet?user_id={st.session_state.user_id}"
        )
        diet_data = diet_response.json()
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        if progress_data:
            latest = progress_data[-1]
            col1.metric("Current Weight", f"{latest['weight']} kg")
            col2.metric("Body Fat", f"{latest['body_fat']}%")
            col3.metric("Progress Trend", "⬆️ Improving" if latest['weight'] < progress_data[0]['weight'] else "⬇️ Needs work")
        
        # Progress charts
        if progress_data:
            st.subheader("Body Metrics Over Time")
            progress_df = pd.DataFrame(progress_data)
            progress_df['date'] = pd.to_datetime(progress_df['date'])
            
            tab1, tab2 = st.tabs(["Weight Trend", "Body Fat"])
            with tab1:
                fig_weight = px.line(
                    progress_df, 
                    x='date', 
                    y='weight', 
                    title="Weight Progress",
                    markers=True
                )
                st.plotly_chart(fig_weight, use_container_width=True)
            
            with tab2:
                fig_bodyfat = px.line(
                    progress_df, 
                    x='date', 
                    y='body_fat', 
                    title="Body Fat Percentage",
                    markers=True
                )
                st.plotly_chart(fig_bodyfat, use_container_width=True)
        
        # Workout analysis
        if workouts_data:
            st.subheader("Workout Analysis")
            workouts_df = pd.DataFrame(workouts_data)
            workouts_df['date'] = pd.to_datetime(workouts_df['date'])
            workouts_df['week'] = workouts_df['date'].dt.isocalendar().week
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Workout Distribution**")
                type_counts = workouts_df['type'].value_counts()
                fig_pie = px.pie(
                    type_counts, 
                    values=type_counts.values, 
                    names=type_counts.index,
                    hole=0.3
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.write("**Weekly Activity**")
                weekly_workouts = workouts_df.groupby('week').size().reset_index(name='count')
                fig_bar = px.bar(
                    weekly_workouts,
                    x='week',
                    y='count',
                    title="Workouts per Week"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Nutrition analysis
        if diet_data:
            st.subheader("Nutrition Overview")
            diet_df = pd.DataFrame(diet_data)
            diet_df['date'] = pd.to_datetime(diet_df['date'])
            
            # Macro nutrients summary
            st.write("**Daily Macronutrients**")
            daily_macros = diet_df.groupby('date')[['protein', 'carbs', 'fat']].sum().reset_index()
            fig_macros = px.line(
                daily_macros.melt(id_vars=['date'], var_name='macro', value_name='grams'),
                x='date',
                y='grams',
                color='macro',
                title="Daily Macronutrient Intake"
            )
            st.plotly_chart(fig_macros, use_container_width=True)
            
            # Meal type distribution
            st.write("**Meal Type Distribution**")
            meal_counts = diet_df['meal_type'].value_counts()
            fig_meals = px.pie(
                meal_counts,
                values=meal_counts.values,
                names=meal_counts.index,
                title="Meal Type Distribution"
            )
            st.plotly_chart(fig_meals, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Make sure you have logged some progress data first")

# Add-ons at bottom
st.divider()
st.caption("FitGPT v1.0 | Your personal AI fitness assistant")