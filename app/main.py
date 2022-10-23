from fastapi import FastAPI

from .routers import word_counter, word_statistics

from app.db.models import word_frequency as word_frequency_models
from .db.schemas import word_frequency as word_frequency_schemas

from .db.base import SessionLocal, engine


app = FastAPI(debug=True)


app.include_router(word_counter.word_counter_router)
app.include_router(word_statistics.word_statistics_router)


# word_frequency_models.Base.metadata.create_all(bind=engine)
# word_frequency_models.Base.metadata.drop_all(bind=engine)


