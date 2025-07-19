import fitdecode
import pandas as pd
from fitdecode.utils import decode_position

def load_fit_file(file) -> pd.DataFrame:
    records = []
    with fitdecode.FitReader(file) as fit:
        for frame in fit:
            if frame.frame_type == fitdecode.FIT_FRAME_DATA and frame.name == "record":
                data = frame.get_values()
                records.append(data)

    df = pd.DataFrame(records)
    df = df[['timestamp', 'position_lat', 'position_long', 'altitude']]
    df = df.dropna()
    df['lat'] = df['position_lat'].apply(decode_position)
    df['lon'] = df['position_long'].apply(decode_position)
    df['elevation'] = df['altitude']
    return df.reset_index(drop=True)
