import streamlit as st
import gpxpy
import pandas as pd
import plotly.graph_objects as go

st.title("🏃 Running – GPX Viewer")

uploaded_gpx = st.file_uploader("Upload a GPX file", type=["gpx"])

if uploaded_gpx:
    gpx = gpxpy.parse(uploaded_gpx.getvalue().decode("utf-8"))

    records = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                records.append({
                    "time": point.time,
                    "lat": point.latitude,
                    "lon": point.longitude,
                    "elevation": point.elevation
                })

    df = pd.DataFrame(records)
    df["time"] = pd.to_datetime(df["time"])
    df["elapsed_sec"] = (df["time"] - df["time"].iloc[0]).dt.total_seconds()
    df["distance"] = df[["lat", "lon"]].apply(lambda row: (row["lat"], row["lon"]), axis=1)
    df["elevation"] = df["elevation"].fillna(method="ffill")

    # Calculate speed in m/s
    df["speed"] = df["elapsed_sec"].diff().shift(-1)
    df["speed"] = 1 / df["speed"].replace(0, float("inf"))  # Not accurate but placeholder

    st.subheader("📊 Summary Stats")
    st.markdown(f"**Elevation Gain:** {df['elevation'].diff().clip(lower=0).sum():.1f} m")
    st.markdown(f"**Total Time:** {df['elapsed_sec'].iloc[-1] / 60:.1f} minutes")

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["elapsed_sec"], y=df["elevation"], name="Elevation", yaxis="y1"))
    fig.add_trace(go.Scatter(x=df["elapsed_sec"], y=df["speed"] * 3.6, name="Speed (km/h)", yaxis="y2"))

    fig.update_layout(
        title="Elevation & Speed Over Time",
        xaxis_title="Elapsed Time (s)",
        yaxis=dict(title="Elevation (m)", side="left"),
        yaxis2=dict(title="Speed (km/h)", overlaying="y", side="right"),
        legend=dict(x=0, y=1),
    )

    st.plotly_chart(fig)