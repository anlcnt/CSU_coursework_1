from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class Author(BaseModel):
    ''' Автор '''
    __tablename__ = "authors"

    books = relationship("Book")
