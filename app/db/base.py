from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore


# DATABASE_URL = "postgresql://user:password@postgresserver/db"
DATABASE_URL = "postgresql://test:test@127.0.0.1:5432/test"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
