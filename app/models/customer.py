from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from app.models.listing import Listing
    from app.models.rental import Rental
    from app.models.payment import Payment
    from app.models.game import Game


class Customer(SQLModel, table=True):
    customerID: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    status: str = "active"

    listings: List["Listing"] = Relationship(back_populates="owner")
    rentals: List["Rental"] = Relationship(back_populates="renter")
    payments: List["Payment"] = Relationship(back_populates="customer")

    def list_game(self, game: "Game", condition: str, price: float, session) -> "Listing":
        from app.models.listing import Listing, Availability
        listing = Listing(gameID=game.gameID, ownerID=self.customerID, condition=condition, price=price, availability=Availability.available)
        session.add(listing)
        session.commit()
        session.refresh(listing)
        return listing

    def rent_game(self, listing: "Listing", session) -> "Rental":
        from app.models.rental import Rental
        from app.models.listing import Availability
        listing.availability = Availability.rented
        rental = Rental(listingID=listing.listingID, renterID=self.customerID, rentalDate=date.today())
        session.add(rental)
        session.add(listing)
        session.commit()
        session.refresh(rental)
        return rental

    def return_game(self, rental: "Rental", amount: float, session) -> "Payment":
        from app.models.payment import Payment
        from app.models.listing import Availability
        rental.returnDate = date.today()
        rental.listing.availability = Availability.available
        payment = Payment(rentalID=rental.rentalID, customerID=self.customerID, amount=amount, payment_date=date.today())
        session.add(rental)
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment
