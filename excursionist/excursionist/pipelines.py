from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DuplicatesPipeline:
    def __init__(self):
        self.offers_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["price"] = self.clean_price(adapter["price"])
        offer_key = self.get_offer_key(adapter)

        if offer_key in self.offers_seen:
            raise DropItem(f"Duplicate offer found: {item!r}")
        else:
            self.offers_seen.add(offer_key)
            return item

    def get_offer_key(self, adapter):
        country = adapter["country"]
        city = adapter["city"]
        price = adapter["price"]
        travel_page = adapter["travel_page"]
        start_date = adapter["start_date"]
        end_date = adapter["end_date"]
        url = adapter["url"]

        return f"{country}-{city}-{price}-{travel_page}-{start_date}-{end_date}-{url}"
    
    @staticmethod
    def clean_price(price):
        return price.replace("from $", "")
