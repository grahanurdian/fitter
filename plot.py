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
    import plotly.graph_objs as go

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['pace'],
        mode='lines',
        name='Pace (min/km)',
        yaxis='y1',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['elevation'],
        mode='lines',
        name='Elevation (m)',
        yaxis='y2',
        line=dict(color='green')
    ))

    fig.update_layout(
        title='Pace & Elevation Over Time',
        xaxis_title='Time',
        yaxis=dict(title='Pace (min/km)', side='left'),
        yaxis2=dict(title='Elevation (m)', overlaying='y', side='right'),
        template='plotly_white'
    )

    return fig

def plot_metrics(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["elapsed_sec"], y=df["elevation"], name="Elevation (m)", yaxis="y1"))
    fig.add_trace(go.Scatter(x=df["elapsed_sec"], y=df["pace"] / 60, name="Pace (min/km)", yaxis="y2"))

    if "heart_rate" in df.columns:
        fig.add_trace(go.Scatter(x=df["elapsed_sec"], y=df["heart_rate"], name="Heart Rate (bpm)", yaxis="y3"))

    fig.update_layout(
        title="Elevation, Pace, and Heart Rate Over Time",
        xaxis=dict(title="Elapsed Time (s)"),
        yaxis=dict(title="Elevation (m)", side="left"),
        yaxis2=dict(title="Pace (min/km)", overlaying="y", side="right", anchor="free", position=0.9),
        yaxis3=dict(title="Heart Rate (bpm)", overlaying="y", side="right", anchor="x", position=1.0),
        legend=dict(x=0, y=1)
    )
    st.plotly_chart(fig, use_container_width=True)
