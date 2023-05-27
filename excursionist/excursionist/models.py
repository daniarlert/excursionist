from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class OfferModel(Base):
    __tablename__ = "offer"

    id: Mapped[int] = mapped_column(primary_key=True)
    origin: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    timestamp: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[str] = mapped_column(nullable=False)
    end_date: Mapped[str] = mapped_column(nullable=False)
    travel_page: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Offer(origin={self.origin}, country={self.country}, city={self.city}, price={self.price}, timestamp={self.timestamp}, start_date={self.start_date}, end_date={self.end_date}, travel_page={self.travel_page}, url={self.url})>"
