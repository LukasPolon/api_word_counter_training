from fastapi import APIRouter


word_statistics_router = APIRouter(prefix="/word_statistics")


@word_statistics_router.get("/")
async def stats():
    return {"Hello": "World - WS"}
