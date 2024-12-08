from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import urllib.request
from pypdf import PdfReader
from src.utils import extract_text_from_pdf, parse_incident_data
from src.clustering import generate_incident_clustering
from src.comparison import generate_location_comparison
from src.pie_chart import generate_nature_pie_chart
import pandas as pd

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def download_pdf_from_url(url):
    try:
        pdf_data = urllib.request.urlopen(urllib.request.Request(url, headers={
            'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        })).read()

        local_directory = "static/uploads"
        create_folder_if_not_exists(local_directory)

        local_file_path = os.path.join(local_directory, os.path.basename(url))

        with open(local_file_path, "wb") as pdf_file:
            pdf_file.write(pdf_data)

        return local_file_path
    except urllib.error.URLError as e:
        print(f"Error downloading the PDF from URL: {url}. Error: {e}")
        return None

def create_folder_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')  
    urls = request.form.get('urls')  

    all_incidents = []

    for file in files:
        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            extracted_text = extract_text_from_pdf(filepath)
            incidents = parse_incident_data(extracted_text)
            all_incidents.extend(incidents)

    if urls:
        url_list = urls.splitlines()
        for url in url_list:
            if url:
                filepath = download_pdf_from_url(url.strip())
                if filepath:
                    extracted_text = extract_text_from_pdf(filepath)
                    incidents = parse_incident_data(extracted_text)
                    all_incidents.extend(incidents)  

    clustering_image = generate_incident_clustering(all_incidents)
    comparison_image = generate_location_comparison(all_incidents)
    custom_image = generate_nature_pie_chart(all_incidents)

    return render_template('visualizations.html', 
                           clustering_image=clustering_image, 
                           comparison_image=comparison_image, 
                           custom_image=custom_image)

if __name__ == '__main__':
    app.run(debug=True)
