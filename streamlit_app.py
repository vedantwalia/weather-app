# streamlit_app.py
import streamlit as st
from weather import get_weather

st.title("🌦 Weather Forecast App")

city = st.text_input("Enter city name")

if city:
    st.write(f"Getting weather for {city}...")
    weather_data = get_weather(city)
    st.write(weather_data)