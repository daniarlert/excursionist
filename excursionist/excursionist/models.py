from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class OfferModel(Base):
    __tablename__ = "offer"

    id: Mapped[int] = mapped_column(primary_key=True)

    origin_city: Mapped[str] = mapped_column()
    origin_country: Mapped[str] = mapped_column()

    destination_city: Mapped[str] = mapped_column()
    destination_country: Mapped[str | None] = mapped_column()

    travel_start_date: Mapped[str] = mapped_column()
    travel_end_date: Mapped[str | None] = mapped_column()

    depart_start_time: Mapped[str | None] = mapped_column()
    depart_arrival_time: Mapped[str | None] = mapped_column()
    depart_airline: Mapped[str | None] = mapped_column()
    depart_stops: Mapped[int | None] = mapped_column()

    return_start_time: Mapped[str | None] = mapped_column()
    return_arrival_time: Mapped[str | None] = mapped_column()
    return_airline: Mapped[str | None] = mapped_column()
    return_stops: Mapped[int | None] = mapped_column()

    price: Mapped[float] = mapped_column()
    travel_page: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()

    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
    )

    def __repr__(self):
        return f"""
            Offer(
                id={self.id},
                origin_city={self.origin_city},
                origin_country={self.origin_country},
                destination_city={self.destination_city},
                destination_country={self.destination_country},
                travel_start_date={self.travel_start_date},
                travel_end_date={self.travel_end_date},
                price={self.price},
                travel_page={self.travel_page},
                url={self.url},
            )
        """
