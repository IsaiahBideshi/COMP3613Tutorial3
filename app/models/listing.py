from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.customer import Customer
    from app.models.rental import Rental


class Availability(str, Enum):
    available = "available"
    rented = "rented"


class Listing(SQLModel, table=True):
    listingID: Optional[int] = Field(default=None, primary_key=True)
    gameID: int = Field(foreign_key="game.gameID")
    ownerID: int = Field(foreign_key="customer.customerID")
    condition: str
    availability: Availability = Availability.available
    price: float

    game: Optional["Game"] = Relationship(back_populates="listings")
    owner: Optional["Customer"] = Relationship(back_populates="listings")
    rentals: List["Rental"] = Relationship(back_populates="listing")
