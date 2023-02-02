from sqlalchemy.orm import relationship

from db.models.base import BaseModel

''' Автор '''
class Author(BaseModel):
	__tablename__ = "authors"

	books = relationship("Book")