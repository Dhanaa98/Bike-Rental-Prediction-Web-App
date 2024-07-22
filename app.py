import pickle
import streamlit as st
import pandas as pd


# Load the model
model = pickle.load(open('model.sav', 'rb'))

st.markdown(
    """
    <style>
    .title-icon {
        display: flex;
        align-items: center;
    }
    .title-icon h1 {
        margin-left: 15px;
    }
    </style>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    <div class="title-icon">
        <i class="fas fa-bicycle fa-2x"></i>
        <h1>Bike Rental Prediction App</h1>
    </div>
    """, unsafe_allow_html=True)


# Season selection
seasons = ['Autumn', 'Spring', 'Summer', 'Winter']
season = st.selectbox('Select Season', seasons)

# Day of the week selection
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_of_week = st.selectbox('Select Day of Week', days_of_week)

# Month selection
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month = st.selectbox('Select Month', months)

# Holiday selection
holiday = st.checkbox('Is it a Holiday?', value=False)
holiday = int(holiday)

# Other parameters
col1, col2, col3 = st.columns(3)
with col1:
    day = st.number_input('Day', value=1)
with col2:
    hour = st.number_input('Hour', value=0)
with col3:
    temperature = st.number_input('Temperature (°C)', value=0.0)
with col1:
    humidity = st.number_input('Humidity (%)', value=0.0)
with col2:
    wind_speed = st.number_input('Wind Speed (m/s)', value=0.0)
with col3:
    visibility = st.number_input('Visibility (10m)', value=0.0)
with col1:
    solar_radiation = st.number_input('Solar Radiation (ML/m2)', value=0.0)
with col2:
    rainfall = st.number_input('Rainfall (mm)', value=0.0)
with col3:
    snowfall = st.number_input('Snowfall (cm)', value=0.0)

# Map season and day_of_week to one-hot encoded columns
season_mapping = {season: 1 for season in seasons}
day_of_week_mapping = {day: 1 for day in days_of_week}
season_encoded = [1 if s == season else 0 for s in seasons]
day_of_week_encoded = [1 if d == day_of_week else 0 for d in days_of_week]
month_encoded = [1 if m == month else 0 for m in months]


# Prepare input data for the model
input_data = {
    'Seasons_Autumn': season_encoded[0], 
    'Seasons_Spring': season_encoded[1], 
    'Seasons_Summer': season_encoded[2], 
    'Seasons_Winter': season_encoded[3], 
    'DayofWeek_Friday': day_of_week_encoded[4], 
    'DayofWeek_Monday': day_of_week_encoded[0], 
    'DayofWeek_Saturday': day_of_week_encoded[5],
    'DayofWeek_Sunday': day_of_week_encoded[6], 
    'DayofWeek_Thursday': day_of_week_encoded[3], 
    'DayofWeek_Tuesday': day_of_week_encoded[1],
    'DayofWeek_Wednesday': day_of_week_encoded[2], 
    'Hour': hour, 
    'Temperature(°C)': temperature, 
    'Humidity(%)': humidity,
    'Wind speed (m/s)': wind_speed, 
    'Visibility (10m)': visibility, 
    'Solar Radiation (MJ/m2)': solar_radiation,
    'Rainfall(mm)': rainfall, 
    'Snowfall (cm)': snowfall, 
    'Month': month_encoded.index(1) + 1, 
    'Day': day,
    'Holiday': holiday
}


# Create DataFrame
input_df = pd.DataFrame([input_data])

# Make prediction
if st.button('Predict Bike Rentals'):
    prediction = model.predict(input_df)
    rounded_prediction = round(prediction[0])
    st.write('Predicted Bike Rentals: ', rounded_prediction)

