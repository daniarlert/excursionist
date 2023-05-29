import scrapy


class FlightsSpider(scrapy.Spider):
    name = "flights"
    allowed_domains = ["www.google.com"]
    start_urls = ["https://www.google.com/travel/flights"]

    def parse(self, response):
        pass
