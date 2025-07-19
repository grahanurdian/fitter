import plotly.graph_objects as go
import pandas as pd

def plot_elevation_speed(df: pd.DataFrame):
    fig = go.Figure()

    # Elevation plot (secondary y-axis)
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['elevation'],
                   name='Elevation (m)', line=dict(color='green'), yaxis='y1')
    )

    # Speed plot
    speed_kmh = df['speed'] * 3.6  # m/s to km/h
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=speed_kmh,
                   name='Speed (km/h)', line=dict(color='blue'), yaxis='y2')
    )

    fig.update_layout(
        title='Elevation & Speed Over Time',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Elevation (m)', side='left'),
        yaxis2=dict(title='Speed (km/h)', overlaying='y', side='right'),
        legend=dict(x=0.01, y=0.99),
        height=500
    )
    return fig


def plot_elevation_pace(df: pd.DataFrame):
    fig = go.Figure()

    # Elevation plot (secondary y-axis)
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['elevation'],
                   name='Elevation (m)', line=dict(color='green'), yaxis='y1')
    )

    # Pace plot
    pace = df['pace'] / 60  # convert to min/km
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=pace,
                   name='Pace (min/km)', line=dict(color='red'), yaxis='y2')
    )

    fig.update_layout(
        title='Elevation & Pace Over Time',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Elevation (m)', side='left'),
        yaxis2=dict(title='Pace (min/km)', overlaying='y', side='right', autorange='reversed'),
        legend=dict(x=0.01, y=0.99),
        height=500
    )
    return fig