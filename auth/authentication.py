from collections import namedtuple
from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError


JWT_SECRET_KEY = 'bb8b55ea4ab4fe42afe2bcc44f1a6af3ec77c5f41fd6db1c4eba6e6693ee0686'
ALGORITHM = 'HS256'
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/users/login')

Claims = namedtuple('Claims', 'id username role exp')


def create_token(id: int, username: str, role: str, expires_delta: timedelta):
    expires = datetime.utcnow() + expires_delta
    claims = Claims(id=id, username=username, role=role, exp=expires)
    return jwt.encode(claims=claims._asdict(), key=JWT_SECRET_KEY, algorithm=ALGORITHM)


def get_token_claims(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        claims = jwt.decode(token=token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return Claims(**claims)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')


UserClaimDependency = Annotated[Claims, Depends(get_token_claims)]
