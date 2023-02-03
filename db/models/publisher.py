from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class Publisher(BaseModel):
    ''' Издательство '''
    __tablename__ = "publishers"

    place = Column(String(255), nullable=False)
    books = relationship("Book", back_populates="publisher")
