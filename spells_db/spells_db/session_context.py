import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PG_URI = 'postgresql://{name}:{password}@{image}:{port}/{name}'


@contextmanager
def session_context(engine=None):
    if engine is None:
        engine = create_engine(PG_URI.format(
            name=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            image=os.environ.get("POSTGRES_HOST"),
            port=os.environ.get("POSTGRES_PORT"),
        ))
    Session = sessionmaker(bind=engine)
    try:
        session = Session()
        yield session
    finally:
        session.rollback()
        session.close()
