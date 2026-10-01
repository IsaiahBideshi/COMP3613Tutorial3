from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.listing import Listing


class Game(SQLModel, table=True):
    gameID: Optional[int] = Field(default=None, primary_key=True)
    title: str
    rating: Optional[str] = None
    platform: Optional[str] = None
    boxart: Optional[str] = None
    genre: Optional[str] = None

    listings: List["Listing"] = Relationship(back_populates="game")
