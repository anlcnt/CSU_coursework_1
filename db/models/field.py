from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class Field(BaseModel):
    ''' Область знаний '''
    __tablename__ = "fields"

    hall_id = Column(Integer, ForeignKey('halls.id'))
    hall = relationship("Hall", back_populates="fields")
    books = relationship("Book", back_populates="field")
