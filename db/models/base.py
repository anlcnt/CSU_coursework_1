from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

now = datetime.now  # Текущее время


class BaseModel(Base):
    '''Базовая модель для всех (кроме выдачи книг) сущностей в базе данных'''
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True,
                primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=now())
    updated_at = Column(DateTime, nullable=False,
                        default=now(), onupdate=now())

    def __repr__(self):
        return f"<{self.__class__.__name__} (id={self.id}, name={self.name})>"
