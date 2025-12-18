import os
import scrapy
from urllib.parse import urljoin

class MedscapeSpider(scrapy.Spider):
    name = "medscape"
    destination_folder = f"../../data/raw/{name}"
    os.makedirs(destination_folder, exist_ok=True)
    allowed_domains = ["emedicine.medscape.com"]
    start_urls = [
        "https://emedicine.medscape.com/article/912781-overview"
    ]

    visited = set()

    def parse(self, response):
        # Prevent loops
        if response.url in self.visited:
            return
        self.visited.add(response.url)

        # Save or extract content
        page_id = response.url.split("/")[-1]
        filename = f"{self.destination_folder}/medscape_{page_id}.html"
        with open(filename, "wb") as f:
            f.write(response.body)

        self.log(f"Saved {filename}")

        # Find "Next" links
        next_links = response.css(
            ".next_btn a::attr(href), .next_section_btn a::attr(href)"
        ).getall()
        
        for href in next_links:
            # Ignore in-page anchors
            if href.startswith("#"):
                continue

            # Build absolute URL
            next_url = urljoin(response.url, href)

            # Respect robots.txt disallow (*-print)
            if next_url.endswith("-print"):
                continue

            self.log(f"Following next page: {next_url}")
            yield response.follow(next_url, callback=self.parse)