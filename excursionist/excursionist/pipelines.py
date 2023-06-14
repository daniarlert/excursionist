import re

from excursionist.db import connect, create_tables, get_session
from excursionist.models import OfferModel
from itemadapter import ItemAdapter


class CleanPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["price"] = self.clean_price(adapter["price"])
        return item

    @staticmethod
    def clean_price(raw_price):
        pattern = r"\d+"
        match = re.search(pattern, raw_price)

        if match:
            return match.group()

        return 0


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
