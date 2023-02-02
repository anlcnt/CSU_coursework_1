from sqlalchemy import Column, Integer, ForeignKey

from db.models.base import Base, now

'''Выдача книг'''
class Lending(Base):
	__tablename__ = "lendings"

	id = Column(Integer, primary_key=True)
	member_id = Column(Integer, ForeignKey("members.id"))
	book_id = Column(Integer, ForeignKey("books.id"))
	lended_at = Column(DateTime, nullable=False, default=now())
	returned_at =  Column(DateTime, default=now())
