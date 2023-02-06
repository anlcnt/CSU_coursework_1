from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import Base, now


class Lending(Base):
    '''Выдача книг'''
    __tablename__ = "lendings"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    lended_at = Column(DateTime, nullable=False, default=now())
    returned_at = Column(DateTime, default=now())

    member = relationship("Member", back_populates="lendings")
    book = relationship("Book", back_populates="lendings")

    def __repr__(self):
        return f"<Lending (id={self.id})>"
