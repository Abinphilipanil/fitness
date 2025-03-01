import os
import sys
import subprocess

# Ensure scikit-learn is installed
try:
    from sklearn.linear_model import LinearRegression
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn"])
    from sklearn.linear_model import LinearRegression

import pandas as pd
import streamlit as st
import datetime
import calendar
def install_required_packages():
    required_packages = ['scikit-learn']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_required_packages()
from sklearn.linear_model import LinearRegression
import numpy as np

# Sample user authentication (You can replace it with a database or OAuth)
USER_CREDENTIALS = {"user": "password123"}  # Example user credentials

# Function to handle user authentication
def authenticate_user():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.sidebar.success("Login successful!")
                # st.experimental_rerun()
            else:
                st.sidebar.error("Invalid credentials. Try again.")
        return False
    else:
        st.sidebar.success(f"Logged in as {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            # st.experimental_rerun()
        return True

# Define missing functions
def display_log_workout():
    st.subheader("Log Workout")
    exercise = st.selectbox("Select Exercise", list(flat_exercise_defaults.keys()))
    sets = st.number_input("Number of Sets", min_value=1, value=flat_exercise_defaults[exercise][0])
    reps = st.number_input("Number of Reps", min_value=1, value=flat_exercise_defaults[exercise][1])
    weight = st.number_input("Weight Used (kg)", min_value=0.0, value=0.0)
    
    if st.button("Save Workout Log"):
        if 'workout_data' not in st.session_state:
            st.session_state.workout_data = pd.DataFrame(columns=["Date", "Exercise", "Sets", "Reps", "Weight"])
        
        new_entry = pd.DataFrame([[datetime.date.today(), exercise, sets, reps, weight]], columns=st.session_state.workout_data.columns)
        st.session_state.workout_data = pd.concat([st.session_state.workout_data, new_entry], ignore_index=True)
        st.success("Workout log saved!")

def display_log_measurement():
    st.subheader("Log Measurements")
    weight = st.number_input("Weight (kg)", min_value=0.0, value=0.0)
    chest = st.number_input("Chest (cm)", min_value=0.0, value=0.0)
    waist = st.number_input("Waist (cm)", min_value=0.0, value=0.0)
    hips = st.number_input("Hips (cm)", min_value=0.0, value=0.0)
    
    if st.button("Save Measurement Log"):
        if 'body_measurements' not in st.session_state:
            st.session_state.body_measurements = pd.DataFrame(columns=["Date", "Weight", "Chest", "Waist", "Hips"])
        
        new_entry = pd.DataFrame([[datetime.date.today(), weight, chest, waist, hips]], columns=st.session_state.body_measurements.columns)
        st.session_state.body_measurements = pd.concat([st.session_state.body_measurements, new_entry], ignore_index=True)
        st.success("Measurement log saved!")

# Calendar function with month selection and proper session state initialization
def display_workout_calendar():
    st.header("Workout Calendar (Streak Tracker)")
    
    # Ensure 'workout_dates' is initialized in session state
    if 'workout_dates' not in st.session_state:
        st.session_state.workout_dates = set()
    
    today = datetime.date.today()

    # Select Year and Month
    year = st.selectbox("Select Year", list(range(today.year - 5, today.year + 5)), index=5)
    month = st.selectbox("Select Month", list(calendar.month_name[1:]), index=today.month - 1)

    month_index = list(calendar.month_name).index(month)
    month_days = calendar.monthrange(year, month_index)[1]
    
    st.write(f"### {month} {year}")

    # Generate calendar layout
    days = [datetime.date(year, month_index, day) for day in range(1, month_days + 1)]
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    cols = [col1, col2, col3, col4, col5, col6, col7]
    
    for i, day in enumerate(days):
        with cols[i % 7]:
            checked = st.checkbox(f"{day.day}", key=f"workout_{day}")
            if checked:
                st.session_state.workout_dates.add(day.strftime('%Y-%m-%d'))
    
    # Display logged workout dates
    st.subheader("Logged Workout Dates")
    if st.session_state.workout_dates:
        st.write(sorted(st.session_state.workout_dates))
    else:
        st.write("No workouts logged yet.")

def display_log_cardio():
    st.subheader("Log Cardio")
    cardio_type = st.selectbox("Type of Cardio", ["Running", "Cycling", "Rowing", "Jump Rope"])
    duration = st.number_input("Duration (minutes)", min_value=0, value=30)
    calories_burned = st.number_input("Calories Burned", min_value=0.0, value=0.0)
    
    if st.button("Save Cardio Log"):
        if 'cardio_data' not in st.session_state:
            st.session_state.cardio_data = pd.DataFrame(columns=["Date", "Cardio Type", "Duration", "Calories Burned"])
        
        new_entry = pd.DataFrame([[datetime.date.today(), cardio_type, duration, calories_burned]], columns=st.session_state.cardio_data.columns)
        st.session_state.cardio_data = pd.concat([st.session_state.cardio_data, new_entry], ignore_index=True)
        st.success("Cardio log saved!")

def display_bmi_calculator():
    st.subheader("BMI Calculator")
    weight = st.number_input("Enter your weight (kg)", min_value=0.0, value=70.0)
    height = st.number_input("Enter your height (cm)", min_value=0.0, value=170.0)

    if height > 0:
        bmi = weight / ((height / 100) ** 2)
        st.write(f"### Your BMI: {bmi:.2f}")

        if bmi < 18.5:
            st.warning("Underweight")
        elif 18.5 <= bmi < 24.9:
            st.success("Normal weight")
        elif 25 <= bmi < 29.9:
            st.warning("Overweight")
        else:
            st.error("Obese")
    else:
        st.error("Height must be greater than zero.")

def display_goal_setting():
    st.subheader("Set Your Fitness Goals")
    goal = st.text_input("Enter Your Goal (e.g., Lose 5kg in 2 months)")
    if st.button("Save Goal"):
        st.session_state['fitness_goal'] = goal
        st.success("Goal saved!")
    if 'fitness_goal' in st.session_state:
        st.write(f"### Current Goal: {st.session_state['fitness_goal']}")

# Define exercise groups and exercises
exercise_defaults = {
    'Chest': {'Bench Press': (3, 8), 'Chest Fly': (3, 8)},
    'Back': {'Pull Up': (3, 8), 'Deadlift': (3, 8)},
    'Legs': {'Squat': (3, 8), 'Leg Press': (3, 8)},
}

flat_exercise_defaults = {exercise: defaults for group in exercise_defaults.values() for exercise, defaults in group.items()}

def suggest_workout_improvements():
    st.subheader("Workout Suggestions")
    if 'workout_data' in st.session_state and not st.session_state.workout_data.empty:
        workout_data = st.session_state.workout_data
        X = workout_data[["Sets", "Reps", "Weight"]].values
        y = np.arange(len(workout_data))  # Just a dummy target variable for now

        model = LinearRegression()
        model.fit(X, y)

        suggestion = model.predict([[3, 8, 10]])  # Example input to get a suggestion
        st.write(f"Suggestion: Increase weight to {suggestion[0]:.2f} kg to improve your workout.")

# Authenticate user before showing app content
if authenticate_user():
    option = st.sidebar.selectbox("Choose a section", ["Home", "Log Workout", "Log Measurements", "Log Cardio", "BMI Calculator", "Exercise Videos","Workout Calendar"])

    if option == "Home":
        st.header("Welcome to the Fitness Tracker App")
        st.write("Use this app to log your workouts and track your progress over time.")
        st.image("https://cdn.pixabay.com/photo/2017/01/03/07/52/weights-1948813_1280.jpg", use_container_width=True)

        display_goal_setting()
        suggest_workout_improvements()

        if 'workout_data' in st.session_state and not st.session_state.workout_data.empty:
            st.subheader("Previous Workout Logs")
            st.dataframe(st.session_state.workout_data.tail())
        if 'body_measurements' in st.session_state and not st.session_state.body_measurements.empty:
            st.subheader("Previous Measurement Logs")
            st.dataframe(st.session_state.body_measurements.tail())
        if 'cardio_data' in st.session_state and not st.session_state.cardio_data.empty:
            st.subheader("Previous Cardio Logs")
            st.dataframe(st.session_state.cardio_data.tail())

    elif option == "Log Workout":
        display_log_workout()
    elif option == "Log Measurements":
        display_log_measurement()
    elif option == "Log Cardio":
        display_log_cardio()
    elif option == "BMI Calculator":
        display_bmi_calculator()
    elif option == "Exercise Videos":
        st.subheader("Exercise Video Tutorials")
        st.markdown("[Bench Press Tutorial](https://www.youtube.com/watch?v=rT7DgCr-3Hk)")
        st.markdown("[Squat Tutorial](https://www.youtube.com/watch?v=aclHkVaku9U)")
        st.markdown("[Deadlift Tutorial](https://www.youtube.com/watch?v=op9kVnSso6Q)")
    elif option == "Workout Calendar":
        display_workout_calendar()
