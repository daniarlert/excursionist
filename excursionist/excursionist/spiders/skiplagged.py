import os

from dotenv import load_dotenv
from excursionist.items import OfferItem
from scrapy import Request, Spider
from scrapy_playwright.page import PageMethod

load_dotenv()


def gen_url(
    origin_city: str,
    destination_city: str | None,
    travel_start_date: str,
) -> str:
    if not destination_city:
        return f"https://skiplagged.com/flights/{origin_city}/{travel_start_date}"
    else:
        return f"https://skiplagged.com/flights/{origin_city}/{destination_city}/{travel_start_date}"


class SkiplaggedExloreSpider(Spider):
    name = "skiplagged-explore"
    allowed_domains = ["skiplagged.com"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.origin_city = os.getenv("ORIGIN_CITY")
        self.travel_start_date = os.getenv("TRAVEL_START_DATE")

        if not self.origin_city:
            raise ValueError("ORIGIN_CITY is not set.")
        if not self.travel_start_date:
            raise ValueError("TRAVEL_START_DATE is not set.")

    def start_requests(self):
        url = gen_url(
            self.origin_city,
            None,
            self.travel_start_date,
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

        # Update the response body with the new HTML.
        updated_html = await page.content()
        response = response.replace(body=updated_html)

        for offer in response.css('ul[id="trip-list-skipsy-tiles"] > li'):
            item = OfferItem()

            item["origin_city"] = os.getenv("ORIGIN_CITY")
            item["origin_country"] = offer.css("span.skipsy-region::text").get()
            item["destination_city"] = offer.css("h2.skipsy-city::text").get()
            item["price"] = offer.css("div.skipsy-cost").get()
            item["travel_start_date"] = self.travel_start_date
            item["travel_page"] = "skiplagged"
            item["url"] = f"https://skiplagged.com{offer.css('a::attr(href)').get()}"

            yield item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
