from fastapi import APIRouter, Depends
from fastapi import Query
from pydantic import BaseModel, Required

from sqlalchemy.orm import Session  # type: ignore

from ..db.crud.word_counter import get_word_count

from ..tools.dependencies import get_session


word_statistics_router = APIRouter(prefix="/word_statistics")


class WordStatisticsResponse(BaseModel):
    word: str
    count: int


@word_statistics_router.get("/")
async def stats(
    word: str = Query(default=Required, max_length=50, regex="^[a-zA-Z]+$"),
    session: Session = Depends(get_session),
):
    """Endpoint responsible of returning a number of word occurrences."""

    word_count = get_word_count(session=session, word_name=word)
    response = WordStatisticsResponse(word=word, count=word_count)
    return response
