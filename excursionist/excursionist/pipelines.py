import re

from excursionist.db import connect, create_tables, get_session
from excursionist.models import OfferModel
from itemadapter import ItemAdapter


class CleanPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["price"] = self.clean_price(adapter["price"], adapter["travel_page"])
        return item

    @staticmethod
    def clean_price(price, travel_page):
        if travel_page == "kayak":
            return price.replace("from $", "")
        elif travel_page == "skiplagged":
            pattern = r">([^<>]+)<"
            match = re.search(pattern, price)
            if match:
                price = match.group(1).strip().replace("€", "")
                return price
            else:
                return price


class SaveToSqlitePipeline:
    def __init__(self) -> None:
        self.engine = connect()
        create_tables(self.engine)

        self.session = get_session(self.engine)

    def process_item(self, item, spider):
        offer = OfferModel(**ItemAdapter(item).asdict())
        self.session.add(offer)
        self.session.commit()

    def close_spider(self, spider):
        self.session.close()
