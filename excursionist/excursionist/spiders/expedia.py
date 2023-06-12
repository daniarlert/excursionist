import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from excursionist.items import OfferItem
from scrapy import Request, Spider
from scrapy_playwright.page import PageMethod

load_dotenv()


# URL
# https://www.expedia.com/Flights-Search?flight-type=on&mode=search&trip=roundtrip&leg1=from%3AAlicante+%28ALC+-+A.+Internacional+de+Alicante%29%2Cto%3AZagreb+%28ZAG+-+Zagreb%29%2Cdeparture%3A06%2F14%2F2023TANYT&options=cabinclass%3Aeconomy&leg2=from%3AZagreb+%28ZAG+-+Zagreb%29%2Cto%3AAlicante+%28ALC+-+A.+Internacional+de+Alicante%29%2Cdeparture%3A06%2F15%2F2023TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY&fromDate=06%2F14%2F2023&toDate=06%2F15%2F2023&d1={start_date}&d2={end_date}
# Items in main > ul:
# <ul class="uitk-typelist uitk-typelist-orientation-stacked uitk-typelist-size-2 uitk-typelist-spacing" data-test-id="listings" role="list">...</ul>
# Items
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
