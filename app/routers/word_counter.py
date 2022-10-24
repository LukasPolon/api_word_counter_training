from datetime import datetime
from dataclasses import dataclass

from fastapi import status
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.engine.base import Engine  # type: ignore

from app.tools.chunk_providers.chunk_provider_protocol import (
    ChunkProviderProtocol,
    FileChunkProviderProtocol,
)
from app.tools.chunk_providers.file_chunk_provider import FileChunkProvider
from app.tools.chunk_providers.plain_chunk_provider import PlainChunkProvider

from ..tools.publishers.normalization_publisher import NormalizationPublisher
from ..tools.publishers.word_counter_publisher import WordCounterPublisher
from ..tools.publishers.publisher_protocol import PublisherProtocol

from ..tools.subscribers.counter_subscriber import CounterSubscriber
from ..db.schemas.word_frequency import WordFrequencyCreate

from ..tools.dependencies import get_engine


word_counter_router = APIRouter(prefix="/word_counter")


@dataclass
class FileHandlerConfig:
    chunk_provider: FileChunkProviderProtocol
    publisher: PublisherProtocol


@dataclass()
class StringHandlerConfig:
    chunk_provider: ChunkProviderProtocol
    publisher: PublisherProtocol


@word_counter_router.post("/", status_code=status.HTTP_201_CREATED)
async def counter(
    file: UploadFile | None = None,
    string_param: str | None = None,
    engine=Depends(get_engine),
):
    start = datetime.now()
    if string_param and file:
        raise ValueError("TOO MUCH")

    if file:
        file_handler_config = __file_handler_factory(engine=engine)
        await __handle_file(
            file=file,
            chunk_provider=file_handler_config.chunk_provider,
            publisher=file_handler_config.publisher,
        )

    if string_param:
        string_handler_config = __string_handler_factory(engine=engine)
        __handle_string_param(
            string_param=string_param,
            chunk_provider=string_handler_config.chunk_provider,
            publisher=string_handler_config.publisher,
        )

    stop = datetime.now()

    return {"OK": f"TIME: {stop - start}"}


def __handle_string_param(
    string_param: str,
    chunk_provider: ChunkProviderProtocol,
    publisher: PublisherProtocol,
):
    chunk_provider.add_data(string_param)
    chunk = chunk_provider.get_chunk()
    publisher.add_data(chunk)
    publisher.run()


async def __handle_file(
    file: UploadFile,
    chunk_provider: FileChunkProviderProtocol,
    publisher: PublisherProtocol,
):
    while file_fragment := await file.read(1024 * 5):
        chunk_provider.add_data(file_fragment)
        new_chunks = chunk_provider.get_chunk()

        for chunk in new_chunks:
            publisher.add_data(data=chunk)
            publisher.run()

    if final_chunk := chunk_provider.get_final_chunk():
        publisher.add_data(data=final_chunk)
        publisher.run()


def __file_handler_factory(engine: Engine) -> FileHandlerConfig:
    chunk_provider = FileChunkProvider()
    counter_subscriber = CounterSubscriber(engine, WordFrequencyCreate)
    word_counter_publisher = WordCounterPublisher()
    word_counter_publisher.add_subscriber(counter_subscriber)
    normalization_publisher = NormalizationPublisher()
    normalization_publisher.add_publisher(word_counter_publisher)

    handler = FileHandlerConfig(
        chunk_provider=chunk_provider, publisher=normalization_publisher
    )
    return handler


def __string_handler_factory(engine: Engine) -> StringHandlerConfig:
    chunk_provider = PlainChunkProvider()
    counter_subscriber = CounterSubscriber(
        engine=engine, create_schema=WordFrequencyCreate
    )
    word_counter_publisher = WordCounterPublisher()
    word_counter_publisher.add_subscriber(counter_subscriber)
    normalization_publisher = NormalizationPublisher()
    normalization_publisher.add_publisher(word_counter_publisher)

    handler = StringHandlerConfig(
        chunk_provider=chunk_provider, publisher=normalization_publisher
    )
    return handler
