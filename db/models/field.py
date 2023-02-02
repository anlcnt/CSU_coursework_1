from sqlalchemy import Column, Integer, ForeignKey

from db.models.base import BaseModel
from db.models.hall import Hall

''' Область знаний '''
class Field(BaseModel):
	__tablename__ = "fields"

	hall_id = Column(Integer, ForeignKey('halls.id'))
	hall = relationship("Hall", back_populates="fields")
	books = relationship("Book", back_populates="field")
