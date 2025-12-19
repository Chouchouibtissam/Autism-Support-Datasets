# Autism Care Centers

## Data Sources

Data was collected from the following publicly accessible websites:

- **Autisme Info Service (France)**  
  Official French public directory of autism-related services  
  🔗 https://annuaire.autismeinfoservice.fr

- **Bookimed (International)**  
  Medical platform listing clinics specialized in autism care  
  🔗 https://us-uk.bookimed.com/clinics/illness=autism/

- **The Autism Service (UK)**  
  Directory of autism support services in the United Kingdom  

Each source has different HTML structures and constraints, requiring **custom extraction strategies**.

---

## Extraction (Web Scraping & Crawling)

- Implemented in **Python** using:
  - `requests`
  - `BeautifulSoup`
  - `pandas`
- Separate scraping scripts were developed for each data source:
  - `france_autism_Scrapping.py`
  - `bookimed_scrapping.py`
  - `theautismservice_scrapping.py`
- Pagination handling was implemented to retrieve **all available pages**
- Polite scraping practices were followed:
  - Delays between requests
  - No authentication or restricted content access
- Extracted attributes include:
  - Center name
  - Region / location
  - Address
  - Phone number
  - Details or website link (when available)

---

## Transformation & Processing

After extraction, multiple data processing steps were applied:

- **Address Normalization**
  - Parsed and split addresses into structured fields:
    - Street number
    - Street name
    - City
    - Region / county
    - Postal code
  - Country-specific formats (France vs UK) handled separately

- **Data Cleaning**
  - Removal of empty or invalid rows
  - Handling missing values

- **Deduplication**
  - Duplicate centers removed to ensure dataset quality


Processed datasets are available in the folder.

---

##  Load & Storage

- Final datasets are stored as **CSV files**
- Chosen because Dataset size is relatively small so no need for additional infrastructure (SQL / NoSQL databases)
- CSV files are ready for:
  - Data analysis with pandas
  - Visualization
  - Further AI model training

---


##  Requirements

To run the scraping scripts:

```bash
pip install requests beautifulsoup4 pandas

python *filename* 
