from sqlalchemy import Column, String, TIMESTAMP

from db.models.base import BaseModel

''' Читатель '''
class Member(BaseModel):
	__tablename__ = "members"

	phone = Column(String(10))  # Номер телефона без префикса
	brith = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())
