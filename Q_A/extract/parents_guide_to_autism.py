import os
import PyPDF2
import csv
import re

pdf_file_path = 'data/raw/parents_guide_to_autism.pdf'
start_page = 13
end_page = 15

destination_folder = f"data/extracted"
os.makedirs(destination_folder, exist_ok=True)

def read_pdf_pages(pdf_path, start_page, end_page):
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page_number in range(start_page - 1, min(end_page, len(reader.pages))):
            page = reader.pages[page_number]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text

# Read the content of the specified pages
result = read_pdf_pages(pdf_file_path, start_page, end_page)

def normalize_text(text):
    # Remove headers like "A PARENT’S GUIDE TO AUTISM11"
    text = re.sub(
        r'\b[A-Z][A-Z\s’\'\-]+AUTISM\d+\b',
        '',
        text
    )
    return text.strip()

def extract_qa(text):
    
    text = normalize_text(text)
    
    # Split the text into questions and answers based on the 'Q:' pattern
    qa_pairs = re.split(r'Q:', text)[1:]

    questions = []
    answers = []

    for qa in qa_pairs:
        parts = re.split(r'\?\s*\n', qa)
        
        # Check if splitting based on "?\s*\n" pattern resulted in more than one part
        if len(parts) > 1:
            question, answer = parts[0], parts[1]
        else:
            # If not, try splitting based on period (.)
            parts = re.split(r'\.\s*\n', qa)
            question, answer = parts[0], parts[1] if len(parts) > 1 else ''
        
        questions.append(question.strip().replace(';', '').replace('\n',''))
        answers.append(answer.strip().replace(';', '').replace('\n',''))

    return zip(questions, answers)

# Extract questions and answers
qa_pairs = extract_qa(result)

with open(f'{destination_folder}/parents_guide_to_autism_extracted_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=";")
    # Write header
    writer.writerow(['Question', 'Answer'])
    # Write data
    writer.writerows(qa_pairs)
