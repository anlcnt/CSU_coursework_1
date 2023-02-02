from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import BaseModel
from db.models.author import Author
from db.models.field import Field
from db.models.publisher import Publisher

''' Книга '''
class Book(BaseModel):
	__tablename__ = "books"

	year = Column(Integer, nullable=False)
	pages = Column(Integer, nullable=False)
	author_id = Column(Integer, ForeignKey('authors.id'))
	publisher_id = Column(Integer, ForeignKey('publishers.id'))
	fields_id = Column(Integer, ForeignKey('fields.id'))
	author = relationship("Author", back_populates="books")
	publisher = relationship("Publisher", back_populates="books")
	field = relationship("Field", back_populates="books")
