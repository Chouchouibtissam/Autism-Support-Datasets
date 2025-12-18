import os
from bs4 import BeautifulSoup, Tag
import csv
import glob
from pathlib import Path

destination_folder = f"data/extracted"
os.makedirs(destination_folder, exist_ok=True)

def extract_medscape_sections(html):
    soup = BeautifulSoup(html, "lxml")
    sections = {}

    # Each Medscape section lives in content_*
    for container in soup.select('div[id^="content_"]'):
        h2 = container.find("h2", recursive=False)
        content = container.find("div", class_="refsection_content")

        # Skip if no meaningful content
        if not h2 or not content:
            continue

        # ---- H2 SECTION ----
        current_h2 = clean_text(h2)
        buffer = []

        for child in content.children:
            if not isinstance(child, Tag):
                continue

            # Stop H2 content when first H3 appears
            if child.name == "h3":
                break

            if child.name in ("p", "ul", "ol"):
                buffer.append(clean_text(child))

        sections[current_h2] = {
            "type": "h2",
            "content": "\n".join(buffer).strip()
        }

        # ---- H3 SUBSECTIONS ----
        current_h3 = None
        buffer = []

        for child in content.children:
            if not isinstance(child, Tag):
                continue

            if child.name == "h3":
                if current_h3:
                    sections[current_h3] = {
                        "type": "h3",
                        "content": "\n".join(buffer).strip()
                    }
                current_h3 = clean_text(child)
                buffer = []
                continue

            if current_h3 and child.name in ("p", "ul", "ol"):
                buffer.append(clean_text(child))

        # Save last h3
        if current_h3:
            sections[current_h3] = {
                "type": "h3",
                "content": "\n".join(buffer).strip()
            }

    return sections

def clean_text(tag):
    return " ".join(tag.stripped_strings)

# ---- loop over all HTML files ----
BASE_DIR = Path("data/raw/medscape")
files = sorted(glob.glob(str(BASE_DIR / "medscape_912781-*.html")))

keyword_content = {}

for file_path in files:
    page_name = Path(file_path).stem.replace("medscape_912781-", "")

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    sections = extract_medscape_sections(html)
    keyword_content.update(sections)

# This maps each question to a keyword for the answer
qa_section_map = {
    # ======================
    # OVERVIEW
    # ======================
    "What is autism spectrum disorder (ASD)?": "Background",
    "What are the signs and symptoms of autism spectrum disorder (ASD)?": "Background",
    "What is the focus of the physical exam for autism spectrum disorder (ASD)?": "Physical Examination",
    "What is the DSM-5 definition of autism spectrum disorder (ASD)?": "Background",
    "Which tests are performed in the workup of autism spectrum disorder (ASD)?": "Approach Considerations",
    "Which imaging studies are performed in the workup of autism spectrum disorder (ASD)?": "Imaging Studies",
    "What types of interventions are used in the treatment of autism spectrum disorder (ASD)?": "Approach Considerations",
    "Which nonpharmacologic therapies are used in the treatment of autism spectrum disorder (ASD)?": "Special Education",
    "Which medications are used in the treatment of autism spectrum disorder (ASD)?": "Pharmacologic Treatment",

    "When does autism spectrum disorder (ASD) typically present?": "Background",
    "What are motion anomalies in children with autism spectrum disorder (ASD)?": "Motion anomalies",
    "What causes autism spectrum disorder (ASD)?": "Etiology",
    "How is autism spectrum disorder (ASD) diagnosed?": "Diagnostic evaluation",
    "How is autism spectrum disorder (ASD) treated?": "Approach Considerations",

    "What are the global trends in the incidence of autism spectrum disorder (ASD)?": "Epidemiology",
    "What is the US prevalence of autism spectrum disorder (ASD)?": "Epidemiology",
    "What is the global prevalence of autism spectrum disorder (ASD)?": "Epidemiology",
    "Which patient groups have the highest prevalence of autism spectrum disorder (ASD)?": "Racial and health disparities",

    "What is the role of faulty parenting in the etiology of autism spectrum disorder (ASD)?": "Etiology",
    "What is the role of obstetric complications in the etiology of autism spectrum disorder (ASD)?": "Prenatal and perinatal risk factors",
    "What is the role of fetal exposure to infectious agents in the etiology of autism spectrum disorder (ASD)?": "Maternal medical conditions",
    "What is the role of genetics in the etiology of autism spectrum disorder (ASD)?": "Genetic and familial factors",
    "What is the role of toxins in the etiology of autism spectrum disorder (ASD)?": "Environmental associations",
    "What is the role of parental age in the etiology of autism spectrum disorder (ASD)?": "Parental age",
    "What is the role of vaccines in the etiology of autism spectrum disorder (ASD)?": "Vaccination",

    "What is the role of neural anomalies in the pathophysiology of autism spectrum disorder (ASD)?": "Neuroanatomic and connectivity findings",
    "What is the role of gamma-amino butyric acid (GABA) in the pathophysiology of autism spectrum disorder (ASD)?": "Neurotransmitter imbalances",
    "What is the role of glutathione (GSH) in the pathophysiology of autism spectrum disorder (ASD)?": "Metabolic and oxidative stress markers",
    "What is the role of N-acetylaspartate (NAA) in the pathophysiology of autism spectrum disorder (ASD)?": "Metabolic and oxidative stress markers",
    "What is the role of metabolic anomalies in the pathophysiology of autism spectrum disorder (ASD)?": "Metabolic and oxidative stress markers",

    "What is the prognosis of autism spectrum disorder (ASD)?": "Prognosis",
    "What are the common comorbidities of autism spectrum disorder (ASD)?": "Comorbid disorders",
    "What is included in patient education about autism spectrum disorder (ASD)?": "Patient Education",
    "What steps should be taken when obtaining informed consent from patients with autism spectrum disorder (ASD)?": "Patient Education",
    "Where can patient education resources on autism spectrum disorder (ASD) be found?": "Patient Education",

    # ======================
    # PRESENTATION
    # ======================
    "Which clinical history findings are characteristic of autism spectrum disorder (ASD)?": "History",
    "How common is developmental regression in autism spectrum disorder (ASD)?": "Developmental regression",
    "What is the role of protodeclarative pointing in predicting a later diagnosis of autism spectrum disorder (ASD)?": "Protodeclarative pointing",
    "Which responses to environmental stimuli are characteristic of autism spectrum disorder (ASD)?": "Environmental stimuli",
    "Which types of social interactions are characteristic of autism spectrum disorder (ASD)?": "Social interactions",
    "Which pain responses are characteristic of autism spectrum disorder (ASD)?": "Pain response",
    "Which speech development findings are characteristic of autism spectrum disorder (ASD)?": "Language",
    "Which types of play are characteristic of autism spectrum disorder (ASD)?": "Play",
    "How do children with autism spectrum disorder (ASD) react to febrile illness?": "Febrile illnesses",
    "What is the Autism Screening Checklist?": "Screening",
    "How are children screened for autism spectrum disorder (ASD)?": "Screening",

    # ======================
    # PHYSICAL EXAM
    # ======================
    "Which body movement findings are characteristic of autism spectrum disorder (ASD)?": "Motor findings",
    "Which physical findings of the head and hands are characteristic of autism spectrum disorder (ASD)?": "Head circumference",
    "How are movements assessed in the physical exam for autism spectrum disorder (ASD)?": "Motor findings",
    "How are stereotypies in the physical exam for autism spectrum disorder (ASD)?": "Motor findings",
    "Which self-injurious behaviors are characteristic of autism spectrum disorder (ASD)?": "Self-injurious behaviors",
    "Which physical findings are characteristic of physical abuse in children with autism spectrum disorder (ASD)?": "Abuse risk",
    "Which physical findings are characteristic of sexual abuse in children with autism spectrum disorder (ASD)?": "Abuse risk",
    "How prevalent is autism spectrum disorder (ASD) among siblings?": "Siblings",

    # ======================
    # DDX
    # ======================
    "What are the DSM-5 diagnostic criteria for autism spectrum disorder (ASD)?": "Diagnostic Considerations",
    "Why should patients be referred to autism specialists for a diagnostic evaluation for autism spectrum disorder (ASD)?": "Diagnostic error and clinician experience",
    "Which screening tests are used to in the diagnostic evaluation for autism spectrum disorder (ASD)?": "Screening",
    "What are cultural considerations when performing a diagnostic evaluation for autism spectrum disorder (ASD)?": "Culture and gender",
    "Which conditions are included in the differential diagnoses of autism spectrum disorder (ASD)?": "Other disorders",

    # ======================
    # WORKUP
    # ======================
    "What is the role of metabolic tests in the workup of autism spectrum disorder (ASD)?": "Laboratory Studies",
    "What is the role of neuroimaging in the workup of autism spectrum disorder (ASD)?": "Neuroimaging",
    "When is electroencephalography indicated in the workup of autism spectrum disorder (ASD)?": "Electroencephalography",
    "What is the role of psychophysiologic assessment in the workup of autism spectrum disorder (ASD)?": "Psychophysiologic assessment",
    "What is the role of polysomnography in the workup of autism spectrum disorder (ASD)?": "Polysomnography",
    "What is the role of genetic tests in the workup of autism spectrum disorder (ASD)?": "Genetic Testing",

    # ======================
    # TREATMENT
    # ======================
    "When is inpatient psychiatric care indicated for autism spectrum disorder (ASD)?": "Inpatient psychiatric care",
    "What is the role of special education in the treatment of autism spectrum disorder (ASD)?": "Special Education",
    "Which types of speech, occupational and physical therapies are used in the treatment of autism spectrum disorder (ASD)?": "Speech, Behavioral, Occupational, and Physical Therapies",
    "What is the role of CBT in the treatment of autism spectrum disorder (ASD)?": "Cognitive behavior therapy (CBT)",
    "What is the role of family therapy in the treatment of autism spectrum disorder (ASD)?": "Family therapy",
    "What is the efficacy of medications for the treatment of autism spectrum disorder (ASD)?": "Pharmacologic Treatment"
}

with open(f'{destination_folder}/medscape_extracted_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(['Question', 'Keyword', 'Answer'])
    for question, keyword in qa_section_map.items():
        if keyword in keyword_content:
            writer.writerow([question, 
                             keyword, 
                             keyword_content[keyword]['content'].strip().replace(';', '').replace('\n',' ')])
        else:
            print(f"Keyword {keyword} not found in scrapped data")

                


