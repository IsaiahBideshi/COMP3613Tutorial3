from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.rental import Rental


class Payment(SQLModel, table=True):
    paymentID: Optional[int] = Field(default=None, primary_key=True)
    rentalID: int = Field(foreign_key="rental.rentalID")
    customerID: int = Field(foreign_key="customer.customerID")
    payment_date: Optional[date] = None
    amount: float

    customer: Optional["Customer"] = Relationship(back_populates="payments")
    rental: Optional["Rental"] = Relationship(back_populates="payments")

    def toJSON(self) -> dict:
        return {
            "paymentID": self.paymentID,
            "rentalID": self.rentalID,
            "customerID": self.customerID,
            "payment_date": str(self.payment_date),
            "amount": self.amount,
        }
