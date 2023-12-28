from fastapi import HTTPException, status
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_object_or_404(db, model: object, **kwargs):
    if len(kwargs) != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Field argument is permitted only one.')

    field_name, value = kwargs.popitem()
    if hasattr(model, field_name):
        found_obj = db.query(model).filter(eval(f'model.{field_name}') == value).first()
        if not found_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{found_obj!r} with {field_name} == {value} not exist.')
        return found_obj
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{model!r} has not field {field_name!r}')
