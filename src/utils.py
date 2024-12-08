import re
from pypdf import PdfReader

# Extract text from the PDF file with date filtering
def extract_text_from_pdf(pdf_file_path):
    reader = PdfReader(pdf_file_path)
    extracted_text = []
    date_pattern = r'\d{1,2}/\d{1,2}/\d{4}' 

    for page_number, page in enumerate(reader.pages):
        page_content = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
        
        if page_content:
            lines = page_content.split("\n")

            if page_number == 0:
                lines = [line for line in lines if re.search(date_pattern, line)]

            for line in lines:
                extracted_text.append(line)

    return extracted_text

# Parse incident records from the extracted text
def parse_incident_data(extracted_text):
    incident_records = []
    for line in extracted_text:
        fields = re.split(r'\s{2,}', line.strip())
        if len(fields) >= 5:
            date_time, incident_number, location, nature, incident_ori = fields[:5]
            
            incident_records.append({
                'date_time': date_time,
                'incident_number': incident_number,
                'location': location,
                'nature': nature,
                'incident_ori': incident_ori
            })
    return incident_records
