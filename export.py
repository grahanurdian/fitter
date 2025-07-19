import gpxpy.gpx
from io import StringIO

def export_gpx(df):
    gpx = gpxpy.gpx.GPX()
    segment = gpxpy.gpx.GPXTrackSegment()
    track = gpxpy.gpx.GPXTrack()
    track.segments.append(segment)
    gpx.tracks.append(track)

    for _, row in df.iterrows():
        point = gpxpy.gpx.GPXTrackPoint(
            latitude=row['lat'],
            longitude=row['lon'],
            elevation=row['elevation'],
            time=row['timestamp_sim']
        )
        segment.points.append(point)

    gpx_file = StringIO()
    gpx_file.write(gpx.to_xml())
    gpx_file.seek(0)
    return gpx_file.getvalue()
