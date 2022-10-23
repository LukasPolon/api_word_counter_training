from sqlalchemy import Column, Integer, String, DateTime, Identity
from sqlalchemy.sql import func

from ..base import Base


class WordFrequency(Base):
    __tablename__ = "word_frequency"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)
    word = Column(String, unique=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
