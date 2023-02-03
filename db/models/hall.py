from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class Hall(BaseModel):
    ''' Область знаний '''
    __tablename__ = "halls"

    fields = relationship("Field", back_populates="hall")
