from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Path, Depends
from fastapi.security import OAuth2PasswordRequestForm

from utils import get_object_or_404, bcrypt_context
from models.user import User, UserCreateReqeust, UserUpdateRequest
from database.connection import DBDependency
from auth.authentication import UserClaimDependency, create_token

router = APIRouter(prefix='/users', tags=['User API'])


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: DBDependency, request_body: UserCreateReqeust) -> dict:
    if get_object_or_404(db, User, username=request_body.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='That username already exist.')
    new_user = User(**request_body.model_dump())
    db.add(new_user)
    db.commit()
    return {'message': 'User created successfully.'}


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(db: DBDependency,
                     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    db_user: User = get_object_or_404(db, User, username=form_data.username)
    if not db_user or bcrypt_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Confirm again Username or Password.')
    token = create_token(id=db_user.id,
                         username=db_user.username,
                         role=db_user.role,
                         expires_delta=timedelta(minutes=60))
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/', status_code=status.HTTP_200_OK)
async def retrieve_user_info(db: DBDependency,
                             user_claims: UserClaimDependency) -> User:
    return get_object_or_404(db, User, id=user_claims.id)


@router.put('/')
async def update_user_info(db: DBDependency,
                           user_claims: UserClaimDependency,
                           request_body: UserUpdateRequest) -> None:
    db_user = get_object_or_404(db, User, id=user_claims.id)
    db_user.update(**request_body.model_dump())  # Todo: Before update operation, consider the unique Email field
    db.add(db_user)
    db.commit()
