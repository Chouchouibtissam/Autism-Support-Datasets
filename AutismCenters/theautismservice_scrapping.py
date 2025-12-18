from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

import time


options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


driver.get("https://www.theautismservice.co.uk/find-a-clinic/")
time.sleep(5)  # wait for JavaScript to load

clinics = []

cards = driver.find_elements(By.CSS_SELECTOR, "li.search-map__clinics-list-item.clinic-card")

for card in cards:
    try:
        name = card.find_element(By.CSS_SELECTOR, "p.clinic-card__title").text
        location = card.find_element(By.CSS_SELECTOR, "span.clinic-card__location").text

        # Open the contact panel
        driver.execute_script("arguments[0].querySelector('button[id$=\"-tab-contact\"]').click();", card)
        time.sleep(0.2)
        contact_panel = card.find_element(By.CSS_SELECTOR, "div[id$='-panel-contact']")
        email = contact_panel.find_element(By.CSS_SELECTOR, "p.clinic-card__email").text
        phone = contact_panel.find_element(By.CSS_SELECTOR, "p.clinic-card__phone").text
        address = " ".join(contact_panel.find_element(By.CSS_SELECTOR, "p.clinic-card__address").text.split("\n"))

        # Open the assessments panel
        driver.execute_script("arguments[0].querySelector('button[id$=\"-tab-assessments\"]').click();", card)
        time.sleep(0.2)
        assessments_panel = card.find_element(By.CSS_SELECTOR, "div[id$='-panel-assessments']")
        assessments = [li.text for li in assessments_panel.find_elements(By.CSS_SELECTOR, "li.clinic-card__assessment")]
        assessments_str = ", ".join(assessments)

        # Open the opening hours panel
        driver.execute_script("arguments[0].querySelector('button[id$=\"-tab-opening-hours\"]').click();", card)
        time.sleep(0.2)
        hours_panel = card.find_element(By.CSS_SELECTOR, "div[id$='-panel-opening-hours']")
        hours = []
        for day_block in hours_panel.find_elements(By.CSS_SELECTOR, "div.clinic-card__opening"):
            day = day_block.find_element(By.CSS_SELECTOR, "p.clinic-card__day").text
            time_text = day_block.find_element(By.CSS_SELECTOR, "p.clinic-card__time").text
            hours.append(f"{day}: {time_text}")
        hours_str = "; ".join(hours)

        clinics.append({
            "Name": name,
            "Location": location,
            "Email": email,
            "Phone": phone,
            "Address": address,
            "Assessments": assessments_str,
            "Opening Hours": hours_str
        })
    except Exception as e:
        print(f"Error: {e}")

driver.quit()

# Save to CSV
df = pd.DataFrame(clinics)
df.to_csv("uk_autism_clinics.csv", index=False)
print("Scraping complete! CSV saved.")
