from datetime import datetime

from pydantic import BaseModel


class WordFrequencyBase(BaseModel):
    word: str


class WordFrequency(WordFrequencyBase):
    id: int
    word: str
    created: datetime

    class Config:
        orm_mode = True


class WordFrequencyCreate(WordFrequencyBase):
    word: str

    class Config:
        orm_mode = True
