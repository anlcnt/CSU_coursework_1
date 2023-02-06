from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class Book(BaseModel):
    ''' Книга '''
    __tablename__ = "books"

    year = Column(Integer, nullable=False)
    pages = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    fields_id = Column(Integer, ForeignKey('fields.id'))

    author = relationship("Author", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    field = relationship("Field", back_populates="books")
    lendings = relationship("Lending", back_populates="book")
