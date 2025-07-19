import streamlit as st
from fit_processing import load_fit_file
from speed_simulation import simulate_speeds
from export import export_gpx
from plot import plot_elevation_speed

st.title("🚴 Fitter – FIT File Speed Adjuster")

uploaded_file = st.file_uploader("Upload a .FIT file", type=["fit"])
avg_speed = st.number_input("Desired Average Speed (km/h)", value=25.0)

if uploaded_file:
    df = load_fit_file(uploaded_file)
    df = simulate_speeds(df, avg_speed)
    st.plotly_chart(plot_elevation_speed(df))

    gpx_data = export_gpx(df)
    st.download_button("Download Adjusted GPX", data=gpx_data, file_name="adjusted.gpx")
