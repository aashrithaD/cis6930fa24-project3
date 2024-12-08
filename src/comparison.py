import pandas as pd
import plotly.graph_objects as go
import os

def generate_location_comparison(incident_data):
    df = pd.DataFrame(incident_data, columns=['date_time', 'incident_number', 'location', 'nature', 'incident_ori'])

    location_counts = df['location'].value_counts()

    fig = go.Figure(data=[go.Bar(x=location_counts.index, y=location_counts.values)])
    
    fig.update_layout(
        title="Incident Count by Location",
        xaxis_title="Location",
        yaxis_title="Incident Count"
    )

    comparison_image_path = 'static/graphs/comparison.png'
    fig.write_image(comparison_image_path)

    return comparison_image_path
