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
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)

    distances = [0]
    times = [0]
    elevation_gain = [0]

    total_gain = 0
    for i in range(1, len(df)):
        coord1 = (df.loc[i-1, 'latitude'], df.loc[i-1, 'longitude'])
        coord2 = (df.loc[i, 'latitude'], df.loc[i, 'longitude'])

        dist = geodesic(coord1, coord2).meters
        time_diff = (df.loc[i, 'timestamp'] - df.loc[i-1, 'timestamp']).total_seconds()
        elev_diff = df.loc[i, 'elevation'] - df.loc[i-1, 'elevation']

        if elev_diff > 0:
            total_gain += elev_diff

        distances.append(dist)
        times.append(time_diff)
        elevation_gain.append(total_gain)

    df['distance_m'] = distances
    df['delta_t'] = times
    df['cumulative_distance_km'] = df['distance_m'].cumsum() / 1000

    # ✅ Correct total distance (in km)
    total_distance_km = df['distance_m'].sum() / 1000
    df['distance'] = total_distance_km

    # ✅ Correct pace (in min/km)
    df['pace'] = (df['delta_t'] / 60) / (df['distance_m'] / 1000)
    df['pace'] = df['pace'].replace([np.inf, -np.inf], np.nan).fillna(method='ffill')

    # ✅ Add elapsed seconds
    df['elapsed_sec'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

    # ✅ Add total elevation gain (same value for all rows, for summary use)
    df['elevation_gain'] = total_gain

    return df