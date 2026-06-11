from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

from database.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float, nullable=False)

    oldbalanceOrg = Column(Float, nullable=False)

    newbalanceOrig = Column(Float, nullable=False)

    is_fraud = Column(Integer, nullable=False)

    fraud_probability = Column(Float, nullable=False)

    transaction_type = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )