from sqlalchemy.engine.base import Engine  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from ..db.base import SessionLocal, engine


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_engine() -> Engine:
    try:
        yield engine
    finally:
        pass
