from fastapi import APIRouter, UploadFile, Form, File, Depends
from sqlalchemy.orm import Session

word_counter_router = APIRouter(prefix="/word_counter")

from app.tools.chunk_providers.file_chunk_provider import FileChunkProvider
from pprint import pprint

from ..tools.publishers.normalization_publisher import NormalizationPublisher
from ..tools.publishers.word_counter_publisher import WordCounterPublisher

from ..tools.subscribers.counter_subscriber import CounterSubscriber
from ..db.schemas.word_frequency import WordFrequencyCreate

from ..tools.dependencies import get_db


@word_counter_router.post("/")
async def counter(file: UploadFile, db: Session = Depends(get_db)):

    chunk_provider = FileChunkProvider()
    counter_subscriber = CounterSubscriber(db, WordFrequencyCreate)
    word_counter_publisher = WordCounterPublisher()
    word_counter_publisher.add_subscriber(counter_subscriber)
    normalization_publisher = NormalizationPublisher()

    normalization_publisher.add_publisher(word_counter_publisher)

    while file_fragment := await file.read(1024):
        chunk_provider.add_data(file_fragment)
        new_chunks = chunk_provider.get_chunk()
        for chunk in new_chunks:
            normalization_publisher.add_data(data=chunk)
            normalization_publisher.run()

    if final_chunk := chunk_provider.get_final_chunk():
        normalization_publisher.add_data(data=final_chunk)
        normalization_publisher.run()
    return {"Hello": "World - WC"}
