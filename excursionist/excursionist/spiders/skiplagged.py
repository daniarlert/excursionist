import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod

from excursionist.items import OfferItem

load_dotenv()


def gen_url(start_date):
    origin = os.getenv("ORIGIN_CITY", "ALC")
    destination = os.getenv("DESTINATION_CITY", "anywhere")
    if destination == "anywhere":
        return f"https://skiplagged.com/flights/{origin}/{start_date}"
    else:
        return f"https://skiplagged.com/flights/{origin}/{destination}/{start_date}"


class SkiplaggedSpider(Spider):
    name = "skiplagged"
    allowed_domains = ["skiplagged.com"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_date = os.getenv(
            "START_DATE", (datetime.now() + timedelta(days=23)).strftime("%Y-%m-%d")
        )

    def start_requests(self):
        url = gen_url(
            self.start_date,
        )

        yield Request(
            url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", 'ul[id^="trip-list-skipsy-tiles"]'),
                ],
                "errback": self.errback,
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        updated_html = await page.content()
        response = response.replace(body=updated_html)

        for offer in response.css('ul[id="trip-list-skipsy-tiles"] > li'):
            item = OfferItem()

            item["origin"] = os.getenv("ORIGIN_CITY", "ALC")
            item["country"] = offer.css("span.skipsy-region::text").get()
            item["city"] = offer.css("h2.skipsy-city::text").get()
            item["price"] = offer.css("div.skipsy-cost").get()
            item["timestamp"] = datetime.utcnow().isoformat()
            item["start_date"] = self.start_date
            item["travel_page"] = "skiplagged"
            item["url"] = f"https://skiplagged.com{offer.css('a::attr(href)').get()}"

            yield item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
