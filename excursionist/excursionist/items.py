from scrapy import Field, Item


class OfferItem(Item):
    origin_city = Field()
    origin_country = Field()
    destination_city = Field()
    destination_country = Field(default=None)
    travel_start_date = Field()
    travel_end_date = Field()
    depart_start_time = Field(default=None)
    depart_arrival_time = Field(default=None)
    depart_airline = Field(default=None)
    depart_stops = Field(default=None)
    return_start_time = Field(default=None)
    return_arrival_time = Field(default=None)
    return_airline = Field(default=None)
    return_stops = Field(default=None)
    price = Field()
    travel_page = Field()
    url = Field()
