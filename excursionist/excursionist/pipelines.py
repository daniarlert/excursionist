from itemadapter import ItemAdapter

from excursionist.db import create_tables, connect, get_session
from excursionist.models import OfferModel


class CleanPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["price"] = self.clean_price(adapter["price"])
        return item

    @staticmethod
    def clean_price(price):
        return price.replace("from $", "")


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
