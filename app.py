import streamlit as st
from fit_processing import load_fit_file, adjust_timestamps
from speed_simulation import simulate_speeds
from export import export_gpx
from plot import plot_elevation_speed
from datetime import datetime, timedelta, time

st.title("🚴 Fitter – FIT File Speed Adjuster")

uploaded_file = st.file_uploader("Upload a .FIT file", type=["fit"])
avg_speed = st.number_input("Desired Average Speed (km/h)", value=25.0)

# Adjust start time
st.subheader("Adjust Start Time")

if uploaded_file:
    df = load_fit_file(uploaded_file)

    # Let user input hour and minute
    hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=6)
    minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

    # Create custom start time
    min_date = df['timestamp'].dt.date.min()
    custom_start_time = datetime.combine(min_date, time(hour, minute))

    # Apply timestamp shift
    df = adjust_timestamps(df, custom_start_time)

    df = simulate_speeds(df, avg_speed)
    st.plotly_chart(plot_elevation_speed(df))

    gpx_data = export_gpx(df)
    formatted_datetime = custom_start_time.strftime("%Y%m%d_%H%M%S")
    file_name = f"adjusted_{formatted_datetime}.gpx"
    st.download_button("Download Adjusted GPX", data=gpx_data, file_name=file_name)