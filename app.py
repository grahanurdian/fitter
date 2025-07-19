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
    st.header("🏃‍♀️ Running Summary")
    gpx_file = st.file_uploader("Upload .gpx file", type="gpx")

    if gpx_file:
        df = load_gpx_file(gpx_file)

        st.subheader("📊 Summary")
        total_distance = df['distance'].iloc[-1] / 1000
        avg_pace = df['pace'].mean()  # in sec/km
        minutes = int(avg_pace // 60)
        seconds = int(avg_pace % 60)
        elevation_gain = df['elevation'].diff().clip(lower=0).sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Distance", f"{total_distance:.2f} km")
        col2.metric("Avg Pace", f"{minutes}:{seconds:02d} /km")
        col3.metric("Elevation Gain", f"{elevation_gain:.0f} m")

        st.subheader("📈 Charts")
        plot_metrics(df)