import fitdecode
import pandas as pd

def load_fit_file(file) -> pd.DataFrame:
    records = []
    with fitdecode.FitReader(file) as fit:
        for frame in fit:
            if frame.frame_type == fitdecode.FIT_FRAME_DATA and frame.name == "record":
                data = {}
                for field in frame.fields:
                    data[field.name] = field.value
                records.append(data)

    df = pd.DataFrame(records)

    # Only keep necessary columns if they exist
    for col in ['timestamp', 'position_lat', 'position_long', 'altitude']:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col} in FIT file")

    df = df.dropna(subset=['timestamp', 'position_lat', 'position_long', 'altitude'])

    df['lat'] = df['position_lat'].apply(decode_position)
    df['lon'] = df['position_long'].apply(decode_position)
    df['elevation'] = df['altitude']

    return df.reset_index(drop=True)

def decode_position(raw_value):
    """Decode raw position value to degrees."""
    return raw_value * (180 / 2**31)

def adjust_timestamps(df, new_start_time):
    # Ensure both timestamps are tz-naive
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)

    original_start_time = df['timestamp'].iloc[0]
    time_diff = new_start_time - original_start_time
    df['timestamp'] = df['timestamp'] + time_diff
    return df