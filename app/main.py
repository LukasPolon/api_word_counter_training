from fastapi import FastAPI

from .routers import word_counter, word_statistics

from app.db.models import word_frequency as word_frequency_models

from .db.base import engine


app = FastAPI(debug=True)


app.include_router(word_counter.word_counter_router)
app.include_router(word_statistics.word_statistics_router)
