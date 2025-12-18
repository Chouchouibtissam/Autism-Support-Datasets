import os
import scrapy

class AutismHubSpider(scrapy.Spider):
    name = "autismhub"
    destination_folder = f"../../data/raw/{name}"
    os.makedirs(destination_folder, exist_ok=True)
    allowed_domains = ["autismhub.ie"]
    start_urls = [
        "https://autismhub.ie/ask-autism-hub/"
    ]

    def parse(self, response):
        # Sauvegarder le HTML brut
        with open(f"{self.destination_folder}/ask_autism_hub.html", "wb") as f:
            f.write(response.body)

        self.log("HTML sauvegardé avec succès")
