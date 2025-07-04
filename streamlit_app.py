import streamlit as st
from weather import get_weather, get_coordinates, get_aqi
import plotly.graph_objects as go

st.set_page_config(page_title="Weather App", page_icon="🌤")
st.title("🌤 Weather Forecast App")

city = st.text_input("🏙️ Enter city name", placeholder="e.g. Mumbai")

if city:
    data = get_weather(city)
    if data.get("cod") != 200:
        st.error(f"❌ Error: {data.get('message')}")
    else:
        st.subheader(f"📍 Weather in {data['name']}, {data['sys']['country']}")
        st.metric("🌡 Temperature", f"{data['main']['temp']} °C")
        st.metric("🤗 Feels Like", f"{data['main']['feels_like']} °C")
        st.metric("💧 Humidity", f"{data['main']['humidity']}%")
        st.metric("🌬 Wind Speed", f"{data['wind']['speed']} m/s")
        st.write("**🌈 Conditions:**", data['weather'][0]['description'].title())
    # AQI Section
        lat, lon = get_coordinates(city)
        if lat is not None and lon is not None:
            aqi_data = get_aqi(lat, lon)
            if "list" in aqi_data and aqi_data["list"]:
                aqi = aqi_data["list"][0]["main"]["aqi"]
                aqi_levels = {
                    1: "Good",
                    2: "Fair",
                    3: "Moderate",
                    4: "Poor",
                    5: "Very Poor"
                }
                st.metric("🫁 Air Quality Index (AQI)", f"{aqi} ({aqi_levels.get(aqi, 'Unknown')})")
            else:
                st.info("ℹ️ No AQI data available for this city.")
        else:
            st.info("ℹ️ Could not determine coordinates for AQI.")

        # Display 5-day temperature forecast as a line graph
        forecast = data.get('forecast', [])
        if forecast:
            dates = [item['dt_txt'] for item in forecast]
            temps = [item['main']['temp'] for item in forecast]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=temps, mode='lines+markers', name='🌡 Temperature (°C)', line=dict(color='orange')))
            fig.update_layout(title="📅 5-Day Temperature Forecast", xaxis_title="📆 Date/Time", yaxis_title="🌡 Temperature (°C)", xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ No 5-day forecast data available for this city.")
