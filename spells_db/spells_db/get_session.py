import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PG_URI = 'postgresql://{name}:{password}@{image}:{port}/{name}'


def get_session():
    engine = create_engine(PG_URI.format(
        name=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        image=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
    ))
    Session = sessionmaker(bind=engine)
    return Session()
