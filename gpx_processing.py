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

    # Calculate distance and pace
    distances = []
    times = []

    for i in range(1, len(df)):
        coord1 = (df.loc[i-1, 'latitude'], df.loc[i-1, 'longitude'])
        coord2 = (df.loc[i, 'latitude'], df.loc[i, 'longitude'])

        dist = geodesic(coord1, coord2).meters
        time_diff = (df.loc[i, 'timestamp'] - df.loc[i-1, 'timestamp']).total_seconds()

        distances.append(dist)
        times.append(time_diff)

    distances.insert(0, 0)
    times.insert(0, 0)

    df['distance_m'] = distances
    df['delta_t'] = times

    # Total cumulative distance in kilometers
    df['cumulative_distance_km'] = df['distance_m'].cumsum() / 1000

    # Also add total distance column in km (for summary)
    df['distance'] = df['distance_m'] / 1000

    # Calculate pace in minutes per km
    df['pace'] = df['delta_t'] / 60 / (df['distance_m'] / 1000)
    df['pace'] = df['pace'].replace([np.inf, -np.inf], np.nan).fillna(method='ffill')

    return df