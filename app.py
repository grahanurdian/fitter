import streamlit as st
from fit_processing import load_fit_file
from speed_simulation import simulate_speeds
from export import export_gpx
from plot import plot_elevation_speed
from fit_processing import adjust_timestamps  # Make sure this exists
from datetime import datetime, time

st.set_page_config(page_title="Fitter", layout="centered")
st.title("🚴 Fitter – FIT File Speed Adjuster")

uploaded_file = st.file_uploader("Upload a .FIT file", type=["fit"])
avg_speed = st.number_input("Desired Average Speed (km/h)", value=25.0)

if uploaded_file:
    df = load_fit_file(uploaded_file)
    
    st.subheader("Adjust Start Time")
    min_date = df['timestamp'].dt.date.min()
    date_input = st.date_input("New Date", min_value=min_date, value=min_date)
    time_input = st.time_input("New Time", value=df['timestamp'].dt.time.min())
    new_datetime = datetime.combine(date_input, time_input)

    df = adjust_timestamps(df, new_datetime)
    df = simulate_speeds(df, avg_speed)

    st.plotly_chart(plot_elevation_speed(df))

    # Summary stats
    st.subheader("📊 Summary Stats")
    st.markdown(f"**Elevation Gain:** {df['altitude'].diff().clip(lower=0).sum():.1f} m")
    st.markdown(f"**Simulated Avg Speed:** {df['speed'].mean() * 3.6:.2f} km/h")

    gpx_data = export_gpx(df)
    formatted_datetime = new_datetime.strftime("%Y%m%d_%H%M%S")
    file_name = f"adjusted_{formatted_datetime}.gpx"
    st.download_button("Download Adjusted GPX", data=gpx_data, file_name=file_name)