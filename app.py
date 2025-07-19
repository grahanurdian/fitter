import streamlit as st
from datetime import datetime, timedelta, time
from fit_processing import load_fit_file, adjust_timestamps
from speed_simulation import simulate_speeds
from export import export_gpx
from plot import plot_elevation_speed, plot_elevation_pace
from gpx_processing import load_gpx_file

st.set_page_config(page_title="Fitter", layout="wide")
st.title("🚴‍♂️ Fitter – Activity File Adjuster")

# Sidebar to switch pages
page = st.sidebar.selectbox("Choose Activity", ["Cycling", "Running"])

if page == "Cycling":
    st.header("🚴 Cycling Mode")
    uploaded_file = st.file_uploader("Upload a .FIT file", type=["fit"])
    avg_speed = st.number_input("Desired Average Speed (km/h)", value=25.0)

    if uploaded_file:
        df = load_fit_file(uploaded_file)

        # Adjust start time
        st.subheader("Adjust Start Time")
        min_date = df['timestamp'].dt.date.min()
        date_input = st.date_input("Select Start Date", min_value=min_date, value=min_date)
        hour = st.number_input("Hour", min_value=0, max_value=23, value=6)
        minute = st.number_input("Minute", min_value=0, max_value=59, value=0)
        custom_start_time = datetime.combine(date_input, time(hour, minute))
        df = adjust_timestamps(df, custom_start_time)

        # Simulate speeds
        df = simulate_speeds(df, avg_speed)
        st.plotly_chart(plot_elevation_speed(df))

        # Summary stats
        st.subheader("Summary")
        st.metric("Total Distance (km)", f"{df['distance'].iloc[-1] / 1000:.2f}")
        st.metric("Avg Speed (km/h)", f"{df['speed'].mean():.2f}")
        st.metric("Elevation Gain (m)", f"{df['elevation'].diff().clip(lower=0).sum():.0f}")

        # Export
        gpx_data = export_gpx(df)
        formatted_datetime = custom_start_time.strftime("%Y%m%d_%H%M%S")
        st.download_button("Download Adjusted GPX", data=gpx_data, file_name=f"adjusted_{formatted_datetime}.gpx")

elif page == "Running":
    st.header("🏃 Running Mode")
    uploaded_gpx = st.file_uploader("Upload a .GPX file", type=["gpx"])

    if uploaded_gpx:
        df = load_gpx_file(uploaded_gpx)

        # Plot elevation vs pace
        st.plotly_chart(plot_elevation_pace(df))

        # Summary
        st.subheader("Summary")
        total_distance_km = df['distance'].iloc[-1] / 1000
        avg_pace_sec_per_km = df['pace'].mean()
        avg_pace_min = int(avg_pace_sec_per_km // 60)
        avg_pace_sec = int(avg_pace_sec_per_km % 60)
        st.metric("Total Distance (km)", f"{total_distance_km:.2f}")
        st.metric("Avg Pace", f"{avg_pace_min}:{avg_pace_sec:02d} min/km")
        st.metric("Elevation Gain (m)", f"{df['elevation'].diff().clip(lower=0).sum():.0f}")
