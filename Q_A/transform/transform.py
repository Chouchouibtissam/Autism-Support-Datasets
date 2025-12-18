import os
import pandas as pd
import re
import json

destination_folder = f"data/transformed"
os.makedirs(destination_folder, exist_ok=True)

# Load the three CSV files into dataframes
childmind = pd.read_csv('data/extracted/childmind_extracted_data.csv', usecols=['Question', 'Answer'], delimiter=";")
medscape = pd.read_csv('data/extracted/medscape_extracted_data.csv', usecols=['Question', 'Answer'], delimiter=";")
parent_guide = pd.read_csv('data/extracted/parents_guide_to_autism_extracted_data.csv', usecols=['Question', 'Answer'], delimiter=";")
ask_autism = pd.read_csv('data/extracted/ask_autism_extracted_data.csv', usecols=['Question', 'Answer'], delimiter=";")

# Add a 'Source' column to each dataframe 
childmind['Source'] = 'childmind'
medscape['Source'] = 'medscape'
parent_guide['Source'] = 'parent_guide'
ask_autism['Source'] = 'ask_autism'


# Concatenate the dataframes vertically
concatenated_df = pd.concat([childmind, medscape, parent_guide, ask_autism])

# Reset the index of the concatenated dataframe
concatenated_df.reset_index(drop=True, inplace=True)

# Define a function to replace the patterns in the 'Answer' column
def replace_patterns(answer):
    # Remove patterns like [1], [4,3], [2, 4,3]
    # pattern = r'\[\d+(?:,\s*\d+)*\]'
    pattern = r'\[\s*\d+(?:\s*,\s*\d+)*\s*\]'
    answer = re.sub(pattern, '', answer)
    
    # Remove "See the image " 
    answer = re.sub(r'(?i)\bsee the image\b.*?(?:\.|$)', '', answer)

    answer = re.sub(r'(?i)\bread more\b.*?(?:\.|$)', '', answer)

    # Remove incomplete answers
    answer = re.sub(r':\s*$', '.', answer)

    answer = answer.replace('\u00a0', ' ')

    # Remove footer with URL + page number
    answer = re.sub(
        r"emedicine\.medscape\.com/article/\d+-print",
        "",
        answer
    )
    
    # Remove "The autism Hub Team" from the end of responses with possible references
    answer = re.sub(r' \u2013 The Autism Hub Team.*', '', answer)


    
    return answer

# Droping lines with no answers that might accur from scraping bugs
concatenated_df = concatenated_df.dropna()

print(len(concatenated_df))

# Replacing noisy patterns such as references
concatenated_df['Answer'] = concatenated_df['Answer'].apply(replace_patterns)

# Convert DataFrame to JSON
json_data = concatenated_df.to_json(orient='records')

json_data = json.loads(json_data)

# Specify the file path where you want to save the JSON data
json_file_path = f'{destination_folder}/clean_data.json'

# Write JSON data to the file
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"JSON data has been saved to {json_file_path}")