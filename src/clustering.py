import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
import os

def generate_incident_clustering(incident_data):
    df = pd.DataFrame(incident_data, columns=['date_time', 'incident_number', 'location', 'nature', 'incident_ori'])

    df['nature'] = df['nature'].str.strip().str.lower()  
    
    nature_counts = df['nature'].value_counts().reset_index()
    nature_counts.columns = ['nature', 'count']

    kmeans = KMeans(n_clusters=3) 
    nature_counts['cluster'] = kmeans.fit_predict(nature_counts[['count']])  

    fig = px.scatter(nature_counts, 
                     x='nature', 
                     y='count', 
                     color='cluster',       
                     title="Incident Clustering by Nature vs Count",
                     labels={"nature": "Nature", "count": "Incident Count"})  

    clustering_image_path = 'static/graphs/clustering.png'
    fig.write_image(clustering_image_path)

    return clustering_image_path
