from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.orm import relationship

from db.models.base import BaseModel, now


''' Читатель '''


class Member(BaseModel):
    __tablename__ = "members"

    phone = Column(String(10))  # Номер телефона без префикса
    brith = Column(TIMESTAMP, nullable=False, default=now())

    lengings = relationship("Lending", back_populates="member")
