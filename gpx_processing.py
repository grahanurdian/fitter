# gpx_processing.py
import gpxpy
import gpxpy.gpx    
import pandas as pd
import numpy as np
from datetime import datetime
from geopy.distance import geodesic

def load_gpx_file(uploaded_file):
    gpx = gpxpy.parse(uploaded_file.read().decode("utf-8"))

    data = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'timestamp': point.time
                })

    df = pd.DataFrame(data)

    if df.empty or len(df) < 2:
        raise ValueError("GPX file has insufficient track points.")

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Calculate distance, time delta, and elevation gain
    distances = [0]
    times = [0]
    elev_gain = [0]

    total_gain = 0

    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        # Distance
        coord1 = (prev['latitude'], prev['longitude'])
        coord2 = (curr['latitude'], curr['longitude'])
        dist = geodesic(coord1, coord2).meters

        # Time delta
        delta_t = (curr['timestamp'] - prev['timestamp']).total_seconds()

        # Elevation gain
        gain = max(0, curr['elevation'] - prev['elevation'])
        total_gain += gain

        distances.append(dist)
        times.append(delta_t)
        elev_gain.append(gain)

    df['distance_m'] = distances
    df['delta_t'] = times
    df['cumulative_distance_km'] = np.cumsum(distances) / 1000
    df['elapsed_sec'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

    # Use sum of all distances as total distance (same value for summary)
    total_distance_km = sum(distances) / 1000
    df['distance'] = total_distance_km

    # Calculate pace (min/km)
    pace = []
    for i in range(len(df)):
        d = df.loc[i, 'distance_m'] / 1000
        t = df.loc[i, 'delta_t'] / 60
        p = t / d if d > 0 else np.nan
        pace.append(p)

    df['pace'] = pd.Series(pace).fillna(method='ffill').replace([np.inf, -np.inf], np.nan)

    # Elevation gain: total (for summary), cumulative column if needed
    df['elevation_gain'] = total_gain

    return df