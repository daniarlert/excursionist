import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod

from excursionist.items import OfferItem


def gen_url(start_date, end_date):
    origin = os.getenv("ORIGIN_CITY", "ALC")
    destination = os.getenv("DESTINATION_CITY", "anywhere")
    return f"https://www.kayak.com/explore/{origin}-{destination}/{start_date.replace('-', '')},{end_date.replace('-', '')}"


class KayakSpider(Spider):
    name = "kayak"
    allowed_domains = ["www.kayak.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_date = os.getenv("START_DATE", datetime.now().strftime("%Y-%m-%d"))
        self.end_date = os.getenv(
            "END_DATE", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        )

    def start_requests(self):
        url = gen_url(
            self.start_date,
            self.end_date,
        )

        yield Request(
            url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", 'button[id$="showMoreButton"]'),
                ],
                "errback": self.errback,
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        while True:
            load_more_button = await page.query_selector('button[id$="showMoreButton"]')
            is_hidden = await load_more_button.is_hidden()
            if is_hidden:
                for offer in response.css("div.Explore-GridViewItem"):
                    item = OfferItem()

                    item["origin"] = os.getenv("ORIGIN_CITY", "ALC")
                    item["country"] = offer.css("div.Country__Name::text").get()
                    item["city"] = offer.css("div.City__Name::text").get()
                    item["price"] = offer.css("div.City__Name + div::text").get()
                    item["timestamp"] = datetime.utcnow().isoformat()
                    item["start_date"] = self.start_date
                    item["end_date"] = self.end_date
                    item["travel_page"] = "kayak"
                    item["url"] = response.url

                    yield item

                break  # Break out of the while loop
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
