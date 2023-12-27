from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

DB_FILE_NAME = 'database.db'
DB_URL = f'sqlite:///{DB_FILE_NAME}'
engine = create_engine(url=DB_URL, connect_args={'check_same_thread': False}, echo=True)


def connect():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(bind=engine) as session:
        yield session


DBDependency = Annotated[Session, Depends(get_session)]
