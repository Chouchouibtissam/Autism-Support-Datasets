import os
from bs4 import BeautifulSoup
import csv

html_file_path = 'data/raw/childmind_guide/child_mind.html'
destination_folder = f"data/extracted"
os.makedirs(destination_folder, exist_ok=True)

try:
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
except FileNotFoundError:
    print(f"File '{html_file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
soup = BeautifulSoup(html_content, 'html.parser')

# Create a CSV file
csv_file = open(f'{destination_folder}/childmind_extracted_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file, delimiter=";")
csv_writer.writerow(['Question', 'Answer'])  # Header row

# Iterate through sections with class 'guide-wrapper-block'
for section in soup.find_all('section', class_='guide-wrapper-block'):
    # Extract question and answer from the section
    question = section.find('div', class_='flex-grow').text.strip()
    answer_paragraphs = section.find('div', class_='pl-10').find_all('p')
    answer = ' '.join([p.text.strip() for p in answer_paragraphs])

    #remove , and new line
    question = question.replace(';', '').replace('\n','')
    answer = answer.replace(';', '').replace('\n','')

    # Write to CSV file
    csv_writer.writerow([question, answer])

# Close the CSV file
csv_file.close()
