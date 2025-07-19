# gpx_processing.py
import gpxpy
import pandas as pd
from datetime import datetime

def load_gpx_file(uploaded_file):
    if uploaded_file is None:
        return pd.DataFrame()

    gpx = gpxpy.parse(uploaded_file.read().decode("utf-8"))
    data = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append({
                    'timestamp': point.time,
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation
                })

    df = pd.DataFrame(data)

    # Calculate pace per km (optional to add now or in plotting)
    return df
