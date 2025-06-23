import os
import csv
from PyPDF2 import PdfReader

# set folder and pdfs for conversion
pdf_folder = "pdfs"
pdf_files = ["united_club_tac.pdf", "mileageplus_rules.pdf", "contract_of_carriage.pdf"]
output_csv = "pdf_texts.csv" # result

# function to get text from the pdf 
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        # aggregate text page by page 
        full_text += page.extract_text() or ""
    return full_text.strip()

# loop through all 3 pdfs and write csv
with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Doc_Name", "Content"])

    for pdf_name in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_name)
        text = extract_text_from_pdf(pdf_path)
        writer.writerow([pdf_name, text])