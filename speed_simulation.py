from haversine import haversine
import pandas as pd
from datetime import timedelta

def simulate_speed(gradient, base_mps):
    if gradient > 0:
        return base_mps * (1 - 0.03 * gradient * 100)
    elif gradient < 0:
        return base_mps * (1 + 0.01 * abs(gradient) * 100)
    return base_mps

def simulate_speeds(df: pd.DataFrame, avg_kmh: float) -> pd.DataFrame:
    distances = [0]
    gradients = [0]
    base_mps = avg_kmh / 3.6
    timestamps = [df.loc[0, 'timestamp']]

    for i in range(1, len(df)):
        p1 = (df.loc[i-1, 'lat'], df.loc[i-1, 'lon'])
        p2 = (df.loc[i, 'lat'], df.loc[i, 'lon'])
        elev_diff = df.loc[i, 'elevation'] - df.loc[i-1, 'elevation']
        distance = haversine(p1, p2) * 1000  # meters
        gradient = elev_diff / distance if distance != 0 else 0
        speed = simulate_speed(gradient, base_mps)

        time_diff = timedelta(seconds=(distance / speed if speed != 0 else 1))
        timestamps.append(timestamps[-1] + time_diff)
        distances.append(distance)
        gradients.append(gradient)

    df['distance'] = distances
    df['gradient'] = gradients
    df['sim_speed_mps'] = [simulate_speed(g, base_mps) for g in gradients]
    df['timestamp_sim'] = timestamps
    return df
