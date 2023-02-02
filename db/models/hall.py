from sqlalchemy.orm import relationship

from db.models.base import BaseModel


''' Область знаний '''


class Hall(BaseModel):
    __tablename__ = "halls"

    fields = relationship("Field", back_populates="hall")
