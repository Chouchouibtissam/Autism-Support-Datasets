# Autism Q&A Data Pipeline

This project implements an **data pipeline** to collect, extract, clean, and consolidate
question–answer (Q&A) data about autism spectrum disorder from multiple trusted online sources.

The final output is a **clean, unified JSON dataset**.

---

## Overview

The pipeline consists of three main stages:

1. **Crawling**  
   Scrape raw HTML content from multiple source websites using Scrapy.

2. **Extraction**  
   Parse the raw HTML files and extract structured Q&A pairs into CSV files.

3. **Transformation & Cleaning**  
   Merge all extracted data, clean noise (references, boilerplate, artifacts), and export a final JSON dataset.

All steps are automated via a single script (`run_pipeline.bat` on Windows, `run_pipeline.sh` on Linux/macOS).

---

## Project Structure

```text
.
├── aquisition/
│   └── crawler/
│       ├── scrapy.cfg
│       └── crawler/
│           ├── spiders/
│           │   ├── childmind_guide.py
│           │   ├── autismhub.py
│           │   └── medscape.py
│           └── settings.py
│
├── extract/
│   ├── ask_autism.py
│   ├── childmind.py
│   ├── medscape.py
│   └── parents_guide_to_autism.py
│
├── transform/
│   └── transform.py
│
├── data/
│   ├── raw/            # Raw HTML files from crawling
│   ├── extracted/      # Intermediate CSV files (per source)
│   └── transformed/    # Final cleaned JSON output
│       └── clean_data.json
│
├── requirements.txt
├── run_pipeline.bat    # Windows pipeline runner
├── run_pipeline.sh     # Linux/macOS pipeline runner
└── README.md
```

## Data Sources

The pipeline currently collects data from:

- **[Child Mind Institute](https://childmind.org/guide/parents-guide-to-autism/)**
- **[Medscape](https://emedicine.medscape.com/article/912781-overview)**
- **[Autism Hub / Ask Autism](https://autismhub.ie/ask-autism-hub/)**
- **[Parents’ Guide to Autism](https://www.autismspeaks.org/tool-kit/parents-guide-autism)**

Each source is crawled and extracted independently, then merged into a single dataset.

---

## Running the Pipeline

### Windows

1. Open **Command Prompt** or **PowerShell**
2. Navigate to the project root
3. Run:

```bat
run_pipeline.bat
```

What the script does:

- Creates a virtual environment (`my_venv`) if missing
- Activates it
- Installs dependencies from `requirements.txt`
- Runs crawling, extraction, and transformation steps

---

### Linux / macOS / WSL

1. Open a terminal
2. Navigate to the project root
3. Make the script executable (first time only):

```bash
chmod +x run_pipeline.sh
```

4. Run the pipeline:

```bash
./run_pipeline.sh
```
