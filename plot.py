import plotly.graph_objects as go

def plot_elevation_speed(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp_sim'],
        y=df['elevation'],
        name='Elevation (m)',
        yaxis='y1',
        line=dict(color='green')
    ))

    fig.add_trace(go.Scatter(
        x=df['timestamp_sim'],
        y=df['sim_speed_mps'] * 3.6,  # Convert to km/h
        name='Speed (km/h)',
        yaxis='y2',
        line=dict(color='blue')
    ))

    fig.update_layout(
        title="Simulated Speed vs Elevation",
        yaxis=dict(title='Elevation (m)', side='left'),
        yaxis2=dict(title='Speed (km/h)', overlaying='y', side='right'),
        xaxis_title="Time",
        legend=dict(x=0.01, y=0.99)
    )
    return fig
