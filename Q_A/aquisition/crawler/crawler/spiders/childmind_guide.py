import os
import scrapy

class ChildmindGuideSpider(scrapy.Spider):
    name = "childmind_guide"
    destination_folder = f"../../data/raw/{name}"
    os.makedirs(destination_folder, exist_ok=True)
    allowed_domains = ["childmind.org"]
    start_urls = [
        "https://childmind.org/guide/parents-guide-to-autism/"
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 10,   # robots.txt
        "CONCURRENT_REQUESTS": 1,
    }
    
    def parse(self, response):
        # Save full HTML
        with open(f"{self.destination_folder}/child_mind.html", "wb") as f:
            f.write(response.body)

        self.log("HTML saved successfully")
