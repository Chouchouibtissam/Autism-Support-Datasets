import requests
import os


if not os.path.exists('data'):
    os.makedirs('data')

    
# List of URLs and corresponding filenames
urls = [
    "https://github.com/shaheennamboori/CSV_dataset_for_autism_diagnostics/raw/master/Autism-Child-Data.csv",
    "https://github.com/shaheennamboori/CSV_dataset_for_autism_diagnostics/raw/master/Autism-Adult_Data.csv",
    "https://github.com/shaheennamboori/CSV_dataset_for_autism_diagnostics/raw/master/Autism-Adolescent-Data.csv"
]

filenames = [
    "data/Autism-Child-Data.csv",
    "data/Autism-Adult-Data.csv",
    "data/Autism-Adolescent-Data.csv"
]

# Download each file
for url, filename in zip(urls, filenames):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"File '{filename}' downloaded successfully.")
    else:
        print(f"Failed to download file from '{url}'.")
