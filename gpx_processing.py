import pandas as pd
import gpxpy
import numpy as np
from datetime import timedelta
from geopy.distance import geodesic

def load_gpx_file(uploaded_file):
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

    # Compute distance between consecutive points
    df['distance'] = 0.0
    for i in range(1, len(df)):
        coord1 = (df.loc[i - 1, 'latitude'], df.loc[i - 1, 'longitude'])
        coord2 = (df.loc[i, 'latitude'], df.loc[i, 'longitude'])
        df.at[i, 'distance'] = geodesic(coord1, coord2).meters

    # Compute total distance and duration between timestamps
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
    df['cum_distance'] = df['distance'].cumsum()

    # Avoid division by zero
    df['pace'] = np.where(df['distance'] > 0, df['time_diff'] / (df['distance'] / 1000), np.nan)  # seconds/km
    df['speed'] = np.where(df['time_diff'] > 0, df['distance'] / df['time_diff'], 0)  # m/s

    return df
