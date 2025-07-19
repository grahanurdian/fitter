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
    plots = []

    # Elevation
    elevation_trace = go.Scatter(x=df['timestamp'], y=df['elevation'],
                                 mode='lines', name='Elevation (m)', line=dict(color='brown'))
    plots.append(elevation_trace)

    # Speed or Pace
    if 'speed' in df.columns:
        speed_trace = go.Scatter(x=df['timestamp'], y=df['speed'] * 3.6,
                                 mode='lines', name='Speed (km/h)', line=dict(color='blue'))
        plots.append(speed_trace)
    elif 'pace' in df.columns:
        pace_trace = go.Scatter(x=df['timestamp'], y=df['pace'] / 60,
                                mode='lines', name='Pace (min/km)', line=dict(color='green'))
        plots.append(pace_trace)

    # Heart Rate
    if 'heart_rate' in df.columns:
        hr_trace = go.Scatter(x=df['timestamp'], y=df['heart_rate'],
                              mode='lines', name='Heart Rate (bpm)', line=dict(color='red'))
        plots.append(hr_trace)

    fig = go.Figure(data=plots)
    fig.update_layout(title='Activity Metrics',
                      xaxis_title='Time',
                      yaxis_title='Value',
                      hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)