from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Path

from database.connection import DBDependency
from auth.authentication import UserClaimDependency
from models.todo import Todo, TodoReqeust

router = APIRouter(prefix='/todos', tags=['Todo API'])


@router.get('/', status_code=status.HTTP_200_OK)
async def retrieve_all(db: DBDependency, user_claims: UserClaimDependency):
    return db.query(Todo).filter(Todo.owner_id == user_claims.id)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create(db: DBDependency, user_claims: UserClaimDependency, body: TodoReqeust):
    new_todo: Todo = Todo(owner_id=user_claims.id, **body.model_dump())
    db.add(new_todo)
    db.commit()


@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def retrieve_by_id(db: DBDependency, user_claims: UserClaimDependency, todo_id: Annotated[int, Path(gt=0)]):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user_claims.id).first()


@router.put('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update(db: DBDependency, body: TodoReqeust, todo_id: Annotated[int, Path(gt=0)]) -> None:
    db_todo: Todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user_claims.id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Does not exist.')
    db_todo.update(**body.model_dump())
    db.add(db_todo)
    db.commit()


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: DBDependency, user_claims:UserClaimDependency, todo_id: Annotated[int, Path(gt=0)]) -> None:
    db_todo: Todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user_claims.id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Does not exist.')
    db.delete(db_todo)
    db.commit()
