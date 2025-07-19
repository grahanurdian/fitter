import streamlit as st
from fit_processing import load_fit_file
from speed_simulation import simulate_speeds
from export import export_gpx
from plot import plot_elevation_speed
from datetime import datetime, timedelta

st.title("🚴 Fitter – FIT File Speed Adjuster")

uploaded_file = st.file_uploader("Upload a .FIT file", type=["fit"])
avg_speed = st.number_input("Desired Average Speed (km/h)", value=25.0)

# Adjust start time
st.subheader("Adjust Start Time")

new_date = st.date_input("Select new Start Date", value=datetime.now().date())
new_time = st.time_input("Select new Start Time", value=datetime.now().time())
new_datetime = datetime.combine(new_date, new_time)

if uploaded_file:
    df = load_fit_file(uploaded_file)
    df = simulate_speeds(df, avg_speed)
    st.plotly_chart(plot_elevation_speed(df))

    gpx_data = export_gpx(df)
    gpx_data = export_gpx(df)
    # Format the new start datetime for the filename
    formatted_datetime = new_datetime.strftime("%Y%m%d_%H%M%S")
    file_name = f"adjusted_{formatted_datetime}.gpx"
    st.download_button("Download Adjusted GPX", data=gpx_data, file_name=file_name)