# scrape_bookimed_autism_centers.py
import requests
from bs4 import BeautifulSoup
import csv

URL = "https://us-uk.bookimed.com/clinics/illness=autism/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_html(url):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.text

def parse_clinics(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # Each clinic card
    for article in soup.select("article.px-20"):
        # Name + URL
        a_tag = article.select_one("h3 a")
        name = a_tag.get_text(strip=True) if a_tag else None
        link = "https://us-uk.bookimed.com" + a_tag["href"] if a_tag and a_tag.has_attr("href") else None

        # Location
        loc = article.select_one("span.leading-normal.text-gray-700")
        location = loc.get_text(strip=True) if loc else None

        # Rating + reviews
        rating_tag = article.select_one("span.text-24.font-semibold.text-gray-900")
        rating = rating_tag.get_text(strip=True) if rating_tag else None

        reviews_tag = article.select_one("span.text-gray-600.text-14")
        reviews = reviews_tag.get_text(strip=True) if reviews_tag else None

        # Description
        desc_block = article.select_one("div.leading-normal")
        description = desc_block.get_text(" ", strip=True) if desc_block else None

        # Certifications (list of alt attributes)
        cert_imgs = article.select("div.flex.flex-wrap img[alt]")
        certs = [img["alt"].strip() for img in cert_imgs if img.has_attr("alt")]

        results.append({
            "name": name,
            "url": link,
            "location": location,
            "rating": rating,
            "reviews": reviews,
            "description": description,
            "certifications": "; ".join(certs)
        })
    return results

def save_to_csv(data, filename="bookimed_autism_centers.csv"):
    if not data:
        print("No data found!")
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} clinics to {filename}")

def main():
    html = get_html(URL)
    clinics = parse_clinics(html)
    save_to_csv(clinics)

if __name__ == "__main__":
    main()
