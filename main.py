from fastapi import FastAPI

from database import connection
from routes import todo, user


app = FastAPI()
app.include_router(router=todo.router)
app.include_router(router=user.router)


@app.on_event('startup')
def on_start():
    connection.connect()
