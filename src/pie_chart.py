import pandas as pd
import plotly.express as px
import os

def generate_nature_pie_chart(incident_data):
    df = pd.DataFrame(incident_data, columns=['date_time', 'incident_number', 'location', 'nature', 'incident_ori'])
    
    df['nature'] = df['nature'].str.strip().str.lower()  
    
    nature_counts = df['nature'].value_counts().reset_index()
    nature_counts.columns = ['nature', 'count']
    
    fig = px.pie(nature_counts, 
                 names='nature', 
                 values='count', 
                 title="Incident Distribution by Nature", 
                 labels={'count': 'Incident Count', 'nature': 'Nature'}, 
                 color_discrete_sequence=px.colors.qualitative.Set3) 
    
    fig.update_layout(
        autosize=False,
        width=1000,  
        height=1000, 
        margin=dict(t=50, b=50, l=50, r=50)  
    )
    
    pie_chart_image_path = 'static/graphs/custom.png'
    fig.write_image(pie_chart_image_path)

    return pie_chart_image_path