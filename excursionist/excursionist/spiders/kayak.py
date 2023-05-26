import scrapy
from scrapy_playwright.page import PageMethod

origin = "ALC"
destination = "anywhere"
start_date = "2023-06-25"  # without -
end_date = "2023-07-02"  # without -
url = f"https://www.kayak.com/explore/{origin}-{destination}/{start_date.replace('-', '')},{end_date.replace('-', '')}"


class KayakSpider(scrapy.Spider):
    name = "kayak"
    allowed_domains = ["www.kayak.com"]
    start_urls = [url]

    def start_requests(self):
        yield scrapy.Request(
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
            for destination in response.css("div.Explore-GridViewItem"):
                yield {
                    "country": destination.css("div.Country__Name::text").get(),
                    "name": destination.css("div.City__Name::text").get(),
                    "price": destination.css("div.City__Name + div::text").get(),
                }

            load_more_button = await page.query_selector('button[id$="showMoreButton"]')
            is_hidden = await load_more_button.is_hidden()
            if is_hidden:
                break

            await page.click('button[id$="showMoreButton"]')
            await page.wait_for_selector("div.Explore-GridViewItem", state="attached")
            await page.wait_for_timeout(1000)  # Adjust the delay if necessary

        await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
