import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from excursionist.items import OfferItem
from scrapy import Request, Spider
from scrapy_playwright.page import PageMethod

load_dotenv()


def gen_url(
    origin_city: str,
    destination_city: str,
    start_date: str,
    end_date: str,
) -> str:
    pass


class ExpediaSpider(Spider):
    name = "expedia"
    allowed_domains = ["www.expedia.com"]

    def parse(self, response):
        pass
