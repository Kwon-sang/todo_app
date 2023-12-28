from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.exc import IntegrityError

DB_FILE_NAME = 'database.db'
DB_URL = f'sqlite:///{DB_FILE_NAME}'
engine = create_engine(url=DB_URL, connect_args={'check_same_thread': False}, echo=True)


def connect():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(bind=engine) as session:
        try:
            yield session
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))


DBDependency = Annotated[Session, Depends(get_session)]
