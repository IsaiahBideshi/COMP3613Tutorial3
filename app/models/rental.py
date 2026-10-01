from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from app.models.listing import Listing
    from app.models.customer import Customer
    from app.models.payment import Payment


class Rental(SQLModel, table=True):
    rentalID: Optional[int] = Field(default=None, primary_key=True)
    listingID: int = Field(foreign_key="listing.listingID")
    renterID: int = Field(foreign_key="customer.customerID")
    rentalDate: Optional[date] = None
    returnDate: Optional[date] = None

    listing: Optional["Listing"] = Relationship(back_populates="rentals")
    renter: Optional["Customer"] = Relationship(back_populates="rentals")
    payments: List["Payment"] = Relationship(back_populates="rental")

    def toJSON(self) -> dict:
        return {
            "rentalID": self.rentalID,
            "listingID": self.listingID,
            "renterID": self.renterID,
            "rentalDate": str(self.rentalDate),
            "returnDate": str(self.returnDate),
        }
