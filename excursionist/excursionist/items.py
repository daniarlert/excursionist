from scrapy import Field, Item


class OfferItem(Item):
    """
    The OfferItem class defines the data model for scraped travel offers from the different travel pages supported by the Excursionist project.

    Attributes:
        origin (Field): Origin city of the travel offer.
        country (Field): Destination country of the travel offer.
        city (Field): Destination city of the offer.
        price (Field): Price of the offer in US dollars.
        timestamp (Field): Timestamp of when the offer was scraped.
        start_date (Field): Start date of the travel.
        end_date (Field): End date of the travel.
        travel_page (Field): Name of the travel page where the offer was scraped.
        url (Field): URL of the offer page, or in some cases, the URL of the offers page.
    """

    origin = Field()
    country = Field()
    city = Field()
    price = Field()
    timestamp = Field()
    start_date = Field()
    end_date = Field()
    travel_page = Field()
    url = Field()
