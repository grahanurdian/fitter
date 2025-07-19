import streamlit as st
from fit_processing import load_fit_file
from speed_simulation import simulate_speeds
from export import export_gpx
from plot import plot_elevation_speed
from timestamp_adjustment import adjust_timestamps  # Make sure this exists
from datetime import datetime, time

st.set_page_config(page_title="Fitter – FIT File Speed Adjuster", layout="wide")
st.title("🚴 Fitter – FIT File Speed Adjuster")

uploaded_file = st.file_uploader("Upload a .FIT file", type=["fit"])
avg_speed = st.number_input("Desired Average Speed (km/h)", value=25.0)

# Load file only after upload
if uploaded_file:
    df = load_fit_file(uploaded_file)

    # ----------------- Start Time Adjustment -----------------
    st.subheader("🕒 Adjust Start Time")
    min_date = df['timestamp'].dt.date.min()
    default_time = df['timestamp'].dt.time.min()
    default_datetime = datetime.combine(min_date, default_time)

    selected_date = st.date_input("Select new start date", value=min_date)
    selected_time = st.time_input("Select new start time", value=default_time)
    custom_start_datetime = datetime.combine(selected_date, selected_time)

    # Adjust timestamps
    df = adjust_timestamps(df, custom_start_datetime)

    # ----------------- Simulate Speed -----------------
    df = simulate_speeds(df, avg_speed)

    # ----------------- Summary Stats -----------------
    st.subheader("📊 Summary Statistics")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Distance (km)", f"{df['distance'].iloc[-1] / 1000:.2f}")
        st.metric("Total Elevation Gain (m)", f"{df['elevation'].diff().clip(lower=0).sum():.1f}")
        st.metric("Max Elevation (m)", f"{df['elevation'].max():.1f}")
        st.metric("Min Elevation (m)", f"{df['elevation'].min():.1f}")

    with col2:
        st.metric("Average Speed (km/h)", f"{df['speed'].mean() * 3.6:.2f}")
        st.metric("Max Speed (km/h)", f"{df['speed'].max() * 3.6:.2f}")
        st.metric("Moving Time (min)", f"{df['timestamp'].diff().dt.total_seconds().sum() / 60:.1f}")

    # ----------------- Plot -----------------
    st.subheader("📈 Elevation and Speed")
    st.plotly_chart(plot_elevation_speed(df), use_container_width=True)

    # ----------------- Export -----------------
    st.subheader("📥 Download Adjusted GPX")
    gpx_data = export_gpx(df)
    formatted_datetime = custom_start_datetime.strftime("%Y%m%d_%H%M%S")
    file_name = f"adjusted_{formatted_datetime}.gpx"
    st.download_button("Download Adjusted GPX", data=gpx_data, file_name=file_name, mime="application/gpx+xml")
