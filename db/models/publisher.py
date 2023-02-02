from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


''' Издательство '''


class Publisher(BaseModel):
    __tablename__ = "publishers"

    place = Column(String(255), nullable=False)
    books = relationship("Book", back_populates="publisher")
