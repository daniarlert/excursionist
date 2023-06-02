from scrapy import Field, Item


class OfferItem(Item):
    """
    The OfferItem class defines the data model for scraped travel offers from the different travel pages supported by the Excursionist project.

    Attributes:
        origin (Field): Origin city of the travel offer.
        country (Field): Destination country of the travel offer.
        city (Field): Destination city of the offer.
        price (Field): Price of the offer in US dollars.
        start_date (Field): Start date of the travel.
        end_date (Field): End date of the travel.
        departure_time (Field): Departure time of the flight.
        arrival_time (Field): Arrival time of the flight.
        travel_page (Field): Name of the travel page where the offer was scraped.
        url (Field): URL of the offer page, or in some cases, the URL of the offers page.
        airline (Field): Name of the airline.
    """

    origin = Field()
    country = Field()
    city = Field()
    price = Field()
    start_date = Field()
    end_date = Field()
    departure_time = Field()
    arrival_time = Field()
    travel_page = Field()
    url = Field()
    airline = Field()
