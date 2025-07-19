""import streamlit as st
import gpxpy
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from math import radians, cos, sin, sqrt, atan2

st.title("🏃 Running – GPX Viewer")

# --- Helper Functions ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # radius of Earth in meters
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))

def simulate_speed(distance, duration, gradient):
    # Simulate slower speed when uphill, faster when downhill
    factor = 1 - (gradient / 10)
    factor = max(0.5, min(factor, 1.5))
    speed = (distance / duration) * factor
    return speed

def calculate_pace(speed_mps):
    if speed_mps == 0:
        return float('inf')
    pace_sec = 1000 / (speed_mps * 60)  # pace in min/km
    return pace_sec

# --- GPX Upload ---
uploaded_gpx = st.file_uploader("Upload a GPX file", type=["gpx"])

if uploaded_gpx:
    gpx = gpxpy.parse(uploaded_gpx.getvalue().decode("utf-8"))

    records = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                hr = point.extensions[0].text if point.extensions else None
                records.append({
                    "time": point.time,
                    "lat": point.latitude,
                    "lon": point.longitude,
                    "elevation": point.elevation,
                    "hr": float(hr) if hr and hr.isdigit() else None
                })

    df = pd.DataFrame(records)
    df["time"] = pd.to_datetime(df["time"])
    df["elapsed_sec"] = (df["time"] - df["time"].iloc[0]).dt.total_seconds()
    df["elevation"] = df["elevation"].fillna(method="ffill")

    # Calculate distance
    distances = [0]
    for i in range(1, len(df)):
        dist = haversine(df.lat[i-1], df.lon[i-1], df.lat[i], df.lon[i])
        distances.append(dist)
    df["delta_dist"] = distances
    df["cum_dist"] = df["delta_dist"].cumsum()

    # Gradient
    df["gradient"] = df["elevation"].diff() / df["delta_dist"].replace(0, 1)
    df["gradient"] = df["gradient"].fillna(0).clip(-0.2, 0.2)

    # Simulated speed and pace
    df["duration"] = df["elapsed_sec"].diff().fillna(1)
    df["speed"] = df.apply(lambda row: simulate_speed(row.delta_dist, row.duration, row.gradient), axis=1)
    df["pace"] = df["speed"].apply(calculate_pace)

    # Set desired pace
    desired_pace = st.number_input("🎯 Desired Pace (min/km)", min_value=3.0, max_value=12.0, value=6.0, step=0.1)

    # Set start time manually
    start_time = st.time_input("🕒 Start Time", value=df["time"].iloc[0].time())
    start_date = st.date_input("📅 Start Date", value=df["time"].iloc[0].date())
    start_datetime = datetime.combine(start_date, start_time)
    df["time"] = [start_datetime + timedelta(seconds=sec) for sec in df["elapsed_sec"]]

    # Summary Stats
    st.subheader("📊 Summary Stats")
    total_distance_km = df["cum_dist"].iloc[-1] / 1000
    avg_pace = df["pace"].replace(float('inf'), 0).mean()
    elevation_gain = df["elevation"].diff().clip(lower=0).sum()
    total_time_min = df["elapsed_sec"].iloc[-1] / 60

    st.markdown(f"**Total Distance:** {total_distance_km:.2f} km")
    st.markdown(f"**Average Pace:** {avg_pace:.2f} min/km")
    st.markdown(f"**Elevation Gain:** {elevation_gain:.1f} m")
    st.markdown(f"**Total Time:** {total_time_min:.1f} minutes")

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["elapsed_sec"], y=df["elevation"], name="Elevation", yaxis="y1"))
    fig.add_trace(go.Scatter(x=df["elapsed_sec"], y=df["pace"], name="Pace (min/km)", yaxis="y2"))
    if df["hr"].notnull().any():
        fig.add_trace(go.Scatter(x=df["elapsed_sec"], y=df["hr"], name="Heart Rate", yaxis="y3"))

    fig.update_layout(
        title="Elevation, Pace, and Heart Rate Over Time",
        xaxis_title="Elapsed Time (s)",
        yaxis=dict(title="Elevation (m)", side="left"),
        yaxis2=dict(title="Pace (min/km)", overlaying="y", side="right"),
        yaxis3=dict(title="HR (bpm)", overlaying="y", side="right", position=1),
        legend=dict(x=0, y=1),
    )

    st.plotly_chart(fig)
