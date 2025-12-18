import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://annuaire.autismeinfoservice.fr/recherche/rubrique/rubrique:14/page:{}/"
#rubrique:14 for Diagnostic center, 10 for ressources cente
data = []
page = 1

while True:
    print(f"Scraping page {page}...")
    response = requests.get(base_url.format(page))
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all table rows
    rows = soup.find_all("tr")

    # Filter rows that actually contain center info
    center_rows = [row for row in rows if row.find("td", class_="padding_left")]

    if not center_rows:  # No more data
        break

    for row in center_rows:
        cols = row.find_all("td")
        center_name = cols[0].get_text(strip=True)
        region = cols[1].get_text(strip=True)
        address = cols[2].get_text(strip=True)
        phone = cols[3].get_text(strip=True)
        details_link = cols[4].find("a")["href"] if cols[4].find("a") else ""
        data.append({
            "Center Name": center_name,
            "Region": region,
            "Address": address,
            "Phone": phone,
            "Details Link": "https://annuaire.autismeinfoservice.fr" + details_link
        })

    page += 1
    time.sleep(1)  # polite delay

# Save results
df = pd.DataFrame(data)
df.to_csv("france_autism_centers_Resources.csv", index=False, encoding="utf-8-sig")
print(f"Scraped {len(df)} centers in total!")
