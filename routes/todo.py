from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Path

from database.connection import DBDependency
from models.todo import Todo, TodoReqeust

router = APIRouter(prefix='/todos', tags=['Todos API'])


def get_todo_or_404(session, id) -> Todo:
    todo_db = session.query(Todo).filter(Todo.id == id).first()
    if not todo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'ID #{id} not exist.')
    return todo_db


# Endpoints
@router.get('/', status_code=status.HTTP_200_OK)
async def retrieve_all(db_session: DBDependency):
    return db_session.query(Todo).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create(db_session: DBDependency, body: TodoReqeust):
    new_todo = Todo(**body.model_dump())
    db_session.add(new_todo)
    db_session.commit()


@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def retrieve_by_id(db_session: DBDependency, todo_id: Annotated[int, Path(gt=0)]):
    return get_todo_or_404(db_session, todo_id)


@router.put('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update(db_session: DBDependency, body: TodoReqeust, todo_id: Annotated[int, Path(gt=0)]):
    todo_db = get_todo_or_404(db_session, todo_id)
    todo_db.update(body)
    db_session.add(todo_db)
    db_session.commit()


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(db_session: DBDependency, todo_id: Annotated[int, Path(gt=0)]):
    todo_db = get_todo_or_404(db_session, todo_id)
    db_session.delete(todo_db)
    db_session.commit()
