# [FastAPI] Basic Todo Application API Project

This project is basic todo application using FastAPI.

referenced by FastAPI official document, book(Building Python Web APIs with FastAPI) and udemy online course.

---

## 1. Project Structure
- models
  - `todo.py`
  - `user.py`
- routers
  - `todo.py`
  - `users.py`
- database
  - `connections.py`
- auth
  - `authentication.py`
- `utils.py`
- `main.py` 


## 2. Project Set-up Base
- Python version control management system: **pyenv** (python 3.10)
- Dependencies management system : **poetry**
- Database : **sqlite3**
  
## 3. Features
- **JWT Authentication**
- **Basical CRUD API on User and Todo**
- **Relational DB connection**

## 4. Web API Visual 
<img width="664" alt="image" src="https://github.com/Kwon-sang/todo_app/assets/115248448/0e262854-576d-4f00-821b-ba2d819b1153">

## 5. My Custom Logic
  1. update method in Model(`User` and `Todo` model):
```
    def update(self, **data):
        for name, value in data.items():
            setattr(self, name, value)
```

2. password hashing logic when `User` instanciated dinamically.
```
    # models.user.User
    def __init__(self, **data):
        super().__init__(**data)
        self.password = bcrypt_context.hash(self.password)
``` 
