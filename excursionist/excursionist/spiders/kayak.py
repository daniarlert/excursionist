import os

from dotenv import load_dotenv
from excursionist.items import OfferItem
from scrapy import Request, Spider
from scrapy_playwright.page import PageMethod

load_dotenv()


def gen_url(
    origin_city: str,
    destination_city: str | None,
    start_date: str,
    end_date: str,
) -> str:
    if not destination_city:
        return f"https://www.kayak.com/explore/{origin_city}-anywhere/{start_date.replace('-', '')},{end_date.replace('-', '')}"
    else:
        return f"https://www.kayak.com/flights/{origin_city}-{destination_city}/{start_date}/{end_date}"


class KayakSpider(Spider):
    name = "kayak-explore"
    allowed_domains = ["www.kayak.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.origin_city = os.getenv("ORIGIN_CITY")
        self.start_date = os.getenv("START_DATE")
        self.end_date = os.getenv("END_DATE")

        if not self.origin_city:
            raise ValueError("ORIGIN_CITY is not set.")
        if not self.start_date:
            raise ValueError("START_DATE is not set.")
        if not self.end_date:
            raise ValueError("END_DATE is not set.")

    def start_requests(self):
        url = gen_url(
            self.origin_city,
            None,
            self.start_date,
            self.end_date,
        )

        yield Request(
            url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.Explore-GridViewItem"),
                ],
                "errback": self.errback,
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        while True:
            load_more_button = await page.query_selector('button[id$="showMoreButton"]')
            is_hidden = await load_more_button.is_hidden()

            if is_hidden or not load_more_button:
                for offer in response.css("div.Explore-GridViewItem"):
                    item = OfferItem()

                    item["origin"] = os.getenv("ORIGIN_CITY", "ALC")
                    item["country"] = offer.css("div.Country__Name::text").get()
                    item["city"] = offer.css("div.City__Name::text").get()
                    item["price"] = offer.css("div.City__Name + div::text").get()
                    item["start_date"] = self.start_date
                    item["end_date"] = self.end_date
                    item["travel_page"] = "kayak"
                    item["url"] = response.url

                    yield item

                break  # Break while loop
            else:
                await page.click('button[id$="showMoreButton"]')
                await page.wait_for_timeout(1000)  # Adjust the delay if necessary

                # Update the response object with the new HTML. Since we're not using the normal Scrapy
                # flow, we need to do this manually.
                updated_html = await page.content()
                response = response.replace(body=updated_html)

        await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()


class KayakSpider(Spider):
    name = "kayak"
    allowed_domains = ["www.kayak.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.origin_city = os.getenv("ORIGIN_CITY")
        self.destination_city = os.getenv("DESTINATION_CITY")
        self.start_date = os.getenv("START_DATE")
        self.end_date = os.getenv("END_DATE")
        self.max_requests = int(os.getenv("MAX_REQUESTS", 1))

        if not self.origin_city:
            raise ValueError("ORIGIN_CITY is not set.")
        if not self.destination_city:
            raise ValueError("DESTINATION_CITY is not set.")
        if not self.start_date:
            raise ValueError("START_DATE is not set.")
        if not self.end_date:
            raise ValueError("END_DATE is not set.")

    def start_requests(self):
        url = gen_url(
            self.origin_city,
            self.destination_city,
            self.start_date,
            self.end_date,
        )

        yield Request(
            url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.resultsList"),
                ],
                "errback": self.errback,
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        num_requests = 0

        while True:
            load_more_button = await page.query_selector("div.show-more-button")
            is_hidden = await load_more_button.is_hidden()

            if is_hidden or not load_more_button or num_requests >= self.max_requests:
                for offer in response.css("div.Explore-resultsList"):
                    pass

                break  # Break while loop
            else:
                await page.click("div.show-more-button")
                await page.wait_for_timeout(1000)  # Adjust the delay if necessary

                # Update the response object with the new HTML. Since we're not using the normal Scrapy
                # flow, we need to do this manually.
                updated_html = await page.content()
                response = response.replace(body=updated_html)

        await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
