import sqlite3
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
        origin = adapter["origin"]
        country = adapter["country"]
        city = adapter["city"]
        price = adapter["price"]
        travel_page = adapter["travel_page"]
        start_date = adapter["start_date"]
        end_date = adapter["end_date"]
        url = adapter["url"]

        return f"{origin}-{country}-{city}-{price}-{travel_page}-{start_date}-{end_date}-{url}"

    @staticmethod
    def clean_price(price):
        return price.replace("from $", "")


class SaveToSqlitePipeline:
    def __init__(self) -> None:
        self.con = sqlite3.connect("../offers.db")
        self.cur = self.con.cursor()

        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS offers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            travel_page TEXT NOT NULL,
            url TEXT NOT NULL
        )
        """
        )

    def process_item(self, item, spider):
        self.cur.execute(
            """
            INSERT INTO offers(
                origin,
                country,
                city,
                price,
                timestamp,
                start_date,
                end_date,
                travel_page,
                url
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                item["origin"],
                item["country"],
                item["city"],
                item["price"],
                item["timestamp"],
                item["start_date"],
                item["end_date"],
                item["travel_page"],
                item["url"],
            ),
        )

        self.con.commit()
        return item

    def close_spider(self, spider):
        self.con.close()
