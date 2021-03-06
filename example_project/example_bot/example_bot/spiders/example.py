# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import re
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector

from example_bot.items import ExampleDotComItem

class PexelsScraper(scrapy.Spider):
    name = "pexels"

    # Define the regex we'll need to filter the returned links
    url_matcher = re.compile('^https:\/\/www\.pexels\.com\/photo\/')

    # Create a set that'll keep track of ids we've crawled
    crawled_ids = set()

    def start_requests(self):
        url = "https://www.pexels.com/"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        body = Selector(text=response.body)
        link_extractor = LinkExtractor(allow=PexelsScraper.url_matcher)
        next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]

        # Crawl the filtered links
        for link in next_links:
            yield scrapy.Request(link, self.parse)
        yield ExampleDotComItem(link=link)

    def is_extracted(self, url):
        # Image urls are of type: https://www.pexels.com/photo/asphalt-blur-clouds-dawn-392010/
        id = int(url.split('/')[-2].split('-')[-1])
        if id not in PexelsScraper.crawled_ids:
            PexelsScraper.crawled_ids.add(id)
            return False
        return True
