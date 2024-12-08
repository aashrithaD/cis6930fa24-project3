import unittest
from unittest.mock import patch, MagicMock
from main import app, is_allowed_file, create_folder_if_not_exists 
from src.utils import extract_text_from_pdf, parse_incident_data
from src.clustering import generate_incident_clustering
from src.comparison import generate_location_comparison
from src.pie_chart import generate_nature_pie_chart
import os
from io import BytesIO

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.upload_folder = 'static/uploads'
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def tearDown(self):
        for filename in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_index_page(self):
        """Test if the index page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NormanPD Incident PDF Upload", response.data)

    @patch('main.extract_text_from_pdf')
    @patch('main.parse_incident_data')
    @patch('main.generate_incident_clustering')
    @patch('main.generate_location_comparison')
    @patch('main.generate_nature_pie_chart')
    def test_upload_pdfs(self, mock_generate_nature_pie_chart, mock_generate_location_comparison, mock_generate_incident_clustering, mock_parse_incident_data, mock_extract_text):
        """Test the upload of PDFs and generation of visualizations"""
        
        mock_extract_text.return_value = ['2022-10-01 12:00:00 12345 Downtown Robbery 123']
        mock_parse_incident_data.return_value = [{'date_time': '2022-10-01 12:00:00', 'incident_number': '12345', 'location': 'Downtown', 'nature': 'Robbery', 'incident_ori': '123'}]
        mock_generate_incident_clustering.return_value = '/static/graphs/clustering.png'
        mock_generate_location_comparison.return_value = '/static/graphs/comparison.png'
        mock_generate_nature_pie_chart.return_value = '/static/graphs/pie_chart.png'

        data = {
            'files': (BytesIO(b"Fake PDF content"), 'test.pdf'),
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Incident Visualizations", response.data)
        self.assertIn(b"Clustering of Incidents", response.data)
        self.assertIn(b"Bar chart of incidents by location", response.data)
        self.assertIn(b"Pie Chart of incidents by nature", response.data)

    @patch('main.download_pdf_from_url')
    @patch('main.extract_text_from_pdf')
    @patch('main.parse_incident_data')
    @patch('main.generate_incident_clustering')
    @patch('main.generate_location_comparison')
    @patch('main.generate_nature_pie_chart')
    def test_upload_urls(self, mock_generate_nature_pie_chart, mock_generate_location_comparison, mock_generate_incident_clustering, mock_parse_incident_data, mock_extract_text, mock_download_pdf_from_url):
        """Test the upload of URLs and generation of visualizations"""
        
        # Mock the download and PDF parsing
        mock_download_pdf_from_url.return_value = 'static/uploads/test.pdf'
        mock_extract_text.return_value = ['2022-10-01 12:00:00 12345 Downtown Robbery 123']
        mock_parse_incident_data.return_value = [{'date_time': '2022-10-01 12:00:00', 'incident_number': '12345', 'location': 'Downtown', 'nature': 'Robbery', 'incident_ori': '123'}]
        mock_generate_incident_clustering.return_value = '/static/graphs/clustering.png'
        mock_generate_location_comparison.return_value = '/static/graphs/comparison.png'
        mock_generate_nature_pie_chart.return_value = '/static/graphs/pie_chart.png'

        # Simulate entering a URL
        data = {
            'urls': 'http://example.com/test.pdf\nhttp://example.com/test2.pdf',
        }
        response = self.app.post('/upload', data=data, content_type='application/x-www-form-urlencoded')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Incident Visualizations", response.data)
        self.assertIn(b"Clustering of Incidents", response.data)
        self.assertIn(b"Bar chart of incidents by location", response.data)
        self.assertIn(b"Pie Chart of incidents by nature", response.data)

    def test_is_allowed_file(self):
        """Test the is_allowed_file function"""
        valid_file = 'document.pdf'
        invalid_file = 'document.txt'

        self.assertTrue(is_allowed_file(valid_file))  
        self.assertFalse(is_allowed_file(invalid_file)) 

    def test_parse_incident_data(self):
        """Test the parse_incident_data function"""
        extracted_text = ['11/3/2024 0:01              2024-00016787          3050 YARBROUGH WAY                                      Drowning/Diving/Scuba Accident                             14005']
        incidents = parse_incident_data(extracted_text)
        self.assertEqual(len(incidents), 1)
        self.assertEqual(incidents[0]['incident_number'], '2024-00016787')

if __name__ == '__main__':
    unittest.main()
