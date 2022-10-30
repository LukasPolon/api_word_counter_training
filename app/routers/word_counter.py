import requests

from datetime import datetime
from dataclasses import dataclass

from fastapi import status
from fastapi import APIRouter, UploadFile, Depends, Query, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.engine.base import Engine  # type: ignore

from app.tools.chunk_providers.chunk_provider_protocol import (
    ChunkProviderProtocol,
    BytesChunkProviderProtocol,
)
from app.tools.chunk_providers.bytes_chunk_provider import BytesChunkProvider
from app.tools.chunk_providers.plain_chunk_provider import PlainChunkProvider

from ..tools.publishers.normalization_publisher import NormalizationPublisher
from ..tools.publishers.word_counter_publisher import WordCounterPublisher
from ..tools.publishers.publisher_protocol import PublisherProtocol

from ..tools.subscribers.counter_subscriber import CounterSubscriber
from ..tools.subscribers.counter_subscriber import CounterSubscriberDatabaseManagement
from ..db.schemas.word_frequency import WordFrequencyCreate

from ..tools.dependencies import get_engine

from ..db.crud.word_counter import add_word
from ..db.crud.word_counter import commit_words


word_counter_router = APIRouter(prefix="/word_counter")


@dataclass
class FileHandlerConfig:
    chunk_provider: BytesChunkProviderProtocol
    publisher: PublisherProtocol


@dataclass
class StringHandlerConfig:
    chunk_provider: ChunkProviderProtocol
    publisher: PublisherProtocol


@dataclass
class UrlHandlerConfig:
    chunk_provider: BytesChunkProviderProtocol
    publisher: PublisherProtocol


@word_counter_router.post("/", status_code=status.HTTP_201_CREATED)
async def counter(
    file: UploadFile | None = None,
    string_param: str
    | None = Query(
        default=None, description="Text to analyze", max_length=50, min_length=1
    ),
    url: str | None = Query(default=None, description="URL to file to upload"),
    engine=Depends(get_engine),
):
    """Endpoint responsible from taking the input data and saving each word occurrence in the database."""
    query_params_number = len([param for param in (file, string_param, url) if param])

    if query_params_number > 1:
        raise HTTPException(status_code=400, detail="Too much query parameters")

    if query_params_number == 0:
        raise HTTPException(status_code=400, detail="Query parameter required")

    if url:
        url_handler_config = __url_handler_factory(engine=engine)
        __handle_url(
            url=url,
            chunk_provider=url_handler_config.chunk_provider,
            publisher=url_handler_config.publisher,
        )

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

    return {"Status": "OK"}


def __handle_string_param(
    string_param: str,
    chunk_provider: ChunkProviderProtocol,
    publisher: PublisherProtocol,
):
    chunk_provider.add_data(string_param)
    chunk = chunk_provider.get_chunk()
    publisher.add_data(chunk)
    publisher.run()


def __handle_url(
    url: str, chunk_provider: BytesChunkProviderProtocol, publisher: PublisherProtocol
):

    with requests.get(url, stream=True) as stream:
        for fragment in stream.iter_content(chunk_size=1024):
            chunk_provider.add_data(fragment)
            new_chunks = chunk_provider.get_chunk()

            for chunk in new_chunks:
                publisher.add_data(data=chunk)
                publisher.run()
        if final_chunk := chunk_provider.get_final_chunk():
            publisher.add_data(data=final_chunk)
            publisher.run()


async def __handle_file(
    file: UploadFile,
    chunk_provider: BytesChunkProviderProtocol,
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
    db_management = CounterSubscriberDatabaseManagement(
        add_word=add_word, commit_words=commit_words
    )
    chunk_provider = BytesChunkProvider()
    counter_subscriber = CounterSubscriber(engine, WordFrequencyCreate, db_management)
    word_counter_publisher = WordCounterPublisher()
    word_counter_publisher.add_subscriber(counter_subscriber)
    normalization_publisher = NormalizationPublisher()
    normalization_publisher.add_publisher(word_counter_publisher)

    handler = FileHandlerConfig(
        chunk_provider=chunk_provider, publisher=normalization_publisher
    )
    return handler


def __string_handler_factory(engine: Engine) -> StringHandlerConfig:
    db_management = CounterSubscriberDatabaseManagement(
        add_word=add_word, commit_words=commit_words
    )
    chunk_provider = PlainChunkProvider()
    counter_subscriber = CounterSubscriber(
        engine=engine, create_schema=WordFrequencyCreate, db_management=db_management
    )
    word_counter_publisher = WordCounterPublisher()
    word_counter_publisher.add_subscriber(counter_subscriber)
    normalization_publisher = NormalizationPublisher()
    normalization_publisher.add_publisher(word_counter_publisher)

    handler = StringHandlerConfig(
        chunk_provider=chunk_provider, publisher=normalization_publisher
    )
    return handler


def __url_handler_factory(engine: Engine) -> UrlHandlerConfig:
    db_management = CounterSubscriberDatabaseManagement(
        add_word=add_word, commit_words=commit_words
    )
    chunk_provider = BytesChunkProvider()
    counter_subscriber = CounterSubscriber(
        engine=engine, create_schema=WordFrequencyCreate, db_management=db_management
    )
    word_counter_publisher = WordCounterPublisher()
    word_counter_publisher.add_subscriber(counter_subscriber)
    normalization_publisher = NormalizationPublisher()
    normalization_publisher.add_publisher(word_counter_publisher)

    handler = UrlHandlerConfig(
        chunk_provider=chunk_provider, publisher=normalization_publisher
    )
    return handler
