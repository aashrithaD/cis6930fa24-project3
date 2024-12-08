# cis6930fa24 -- Project 3

Name: AASHRITHA REDDY DONAPATI

# Assignment Description
This project focuses on creating a web application that extracts, parses, and visualizes data from incident reports (in PDF format) using Flask. The primary objective is to enable users to upload multiple PDF files or provide URLs of incident reports, and in turn, generate various visualizations, including clustering, bar charts, and pie charts, based on the extracted incident data. The application processes the incident data by extracting key details such as incident number, location, nature of the incident, and timestamp, and uses this information to generate visualizations that offer valuable insights into incident patterns and trends.

# How to install
To install the required dependencies:  pipenv install

## How to run

1. To execute the project:  
pipenv run python main.py

2. To run the test cases:  
pipenv run python -m pytest -v   

## Project Demo


## Functions

## main.py

1. is_allowed_file(filename):
```sh
Process: Checks if the uploaded file has a valid PDF extension.
Returns: True if the file is a PDF, False otherwise.
```
2. download_pdf_from_url(url):
```sh
Process: Downloads the PDF file from a given URL and saves it locally in the "static/uploads" folder.
Returns: The local path of the saved PDF file.
```
3. create_folder_if_not_exists(directory):
```sh
Process: Creates a folder if it does not exist. This ensures the "static/uploads" directory is available to store the uploaded files.
Returns: None.
```
4. index():
```sh
Process: Renders the homepage (index.html) where users can upload PDF files or provide URLs for incident reports.
Returns: The HTML page for the main interface.
```
5. upload_files():
```sh
Process: Handles the POST request for file uploads. It processes both uploaded PDF files and URLs. For each PDF (either uploaded or downloaded from a URL), the text is extracted, parsed into incident records, and visualizations are generated.
Returns: Renders the visualizations.html template displaying the generated clustering image, comparison chart, and pie chart.
```
## clustering.py

6. generate_incident_clustering():
```sh
Process: Clusters incident data based on the frequency of each incident type (nature) using KMeans and generates a scatter plot to visualize the clustering.
Returns: The file path of the saved clustering plot image (static/graphs/clustering.png).
```
## comparision.py

7. generate_location_comparison():
```sh
Process: Generates a bar chart comparing the count of incidents by location. It first counts the incidents per location and then visualizes the result in a bar chart. The chart is saved as an image for display.
Returns: The file path of the saved comparison plot image (static/graphs/comparison.png).
```
## pie_chart.py

8. generate_nature_pie_chart():
```sh
Process: Generates a pie chart visualizing the distribution of incidents by their nature. It first counts the occurrences of each unique nature in the incident data, and then creates a pie chart to represent this distribution. The chart is saved as an image for display.
Returns: The file path of the saved pie chart image (static/graphs/custom.png).
```
## utils.py

9. extract_text_from_pdf():
```sh
Process: Extracts text from a PDF file, filtering lines that contain date information in the format MM/DD/YYYY. The text is extracted from each page of the PDF, and only lines containing dates are retained for further processing.
Returns: A list of extracted text lines from the PDF, filtered by the presence of a date.
```
10. parse_incident_data():
```sh
Process: Parses the extracted text into structured incident data. It splits each line based on multiple spaces and extracts relevant details such as date_time, incident_number, location, nature, and incident_ori into a dictionary format.
Returns: A list of dictionaries, each containing incident details extracted from the text.
```
## test_app.py

1. setUp(): The setUp() function is part of the test preparation process. It runs before each test method and initializes the testing environment. In this case, it sets up the Flask app’s test client, enabling interaction with the app during tests. It also creates the static/uploads folder if it doesn't already exist, ensuring a directory is available for file uploads during the tests.

2. tearDown(): The tearDown() function is called after each test method runs, cleaning up the testing environment. It deletes any files in the static/uploads directory to ensure the tests start with a clean slate each time. This helps avoid leftover files from affecting subsequent tests.

3. test_index_page(): The test_index_page() function tests the root route (/) of the Flask app to ensure the index page loads correctly. It sends a GET request to the root URL and checks that the response has a status code of 200, indicating the page loaded successfully. Additionally, it checks if the page contains the text "NormanPD Incident PDF Upload," verifying that the correct content is rendered on the page.

4. test_upload_pdfs(): This function tests the functionality of uploading PDFs through the /upload route and generating visualizations. It uses mocks to simulate the behavior of key functions such as extract_text_from_pdf(), parse_incident_data(), and the visualization generation functions (generate_incident_clustering(), generate_location_comparison(), and generate_nature_pie_chart()). The function simulates uploading a PDF file by sending a POST request with fake PDF content. It then checks that the response contains the expected visualizations and has a status code of 200.

5. test_upload_urls(): The test_upload_urls() function tests the functionality of uploading URLs and generating visualizations from the PDF files located at those URLs. It uses mocks to simulate downloading the PDFs, extracting text, parsing incident data, and generating visualizations. The function sends a POST request with a list of URLs and ensures that the response contains the expected visualizations. It also checks that the response status code is 200, indicating the operation was successful.

6. test_is_allowed_file(): The test_is_allowed_file() function tests the is_allowed_file() utility function, which checks whether a file has a valid extension (in this case, PDF). It provides two test files: a valid PDF file (document.pdf) and an invalid text file (document.txt). The test asserts that is_allowed_file() returns True for the valid file and False for the invalid file, ensuring the function correctly filters file types.

7. test_parse_incident_data(): The test_parse_incident_data() function tests the parse_incident_data() function, which converts raw text into structured incident data. It provides an example of extracted text and checks that the parsed result is a list of dictionaries with the correct fields, including incident_number. The test verifies that the function correctly processes the extracted data into structured incident information.

## Bugs:
1. The PDF structure may vary, leading to inconsistent data extraction. For example, if some incident records have additional fields or missing data, the parsing logic may fail or return incomplete results.
2. If any PDF contains non-standard characters (e.g., accented characters, emojis, etc.) or uses non-UTF-8 encoding, it could cause issues during text extraction and parsing.
3. URLs that redirect to a login page or require authentication are not handled. The system will try to download the PDF but will fail silently if the URL is not publicly accessible.
4. If neither a PDF file nor a URL is provided by the user when clicking the upload button, the system will raise an error.

## Assumptions:

1. The uploaded or provided PDFs follow a consistent format with the following required fields: date_time, incident_number, location, nature, and incident_ori.
2. The data is expected to be space-separated, without irregular spacing.
3. The system assumes that incident data extracted from the PDFs will not contain duplicates. Any duplicated incidents are not filtered out during the processing.
4. URLs provided by users are assumed to be well-formed and contain valid PDF links. The system expects one URL per line in the provided input.
5. The system assumes that all incident reports follow the same date format (MM/DD/YYYY), ensuring correct date extraction and filtering.
6. It is assumed that users can provide both URLs and PDF files at once. 
