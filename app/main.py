from fastapi import FastAPI

from .routers import word_counter, word_statistics

app = FastAPI(debug=True)

app.include_router(word_counter.word_counter_router)
app.include_router(word_statistics.word_statistics_router)
