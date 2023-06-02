from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class OfferModel(Base):
    __tablename__ = "offer"

    id: Mapped[int] = mapped_column(primary_key=True)
    origin: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow(),
    )
    start_date: Mapped[str] = mapped_column(nullable=False)
    end_date: Mapped[str] = mapped_column(nullable=True)
    departure_time: Mapped[datetime] = mapped_column(nullable=True)
    arrival_time: Mapped[datetime] = mapped_column(nullable=True)
    travel_page: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    airline: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<OfferModel(origin={self.origin}, country={self.country}, city={self.city}, price={self.price}, timestamp={self.timestamp}, start_date={self.start_date}, end_date={self.end_date}, departure_time={self.departure_time}, arrival_time={self.arrival_time}, travel_page={self.travel_page}, url={self.url}, airline={self.airline})>"
