from fastapi import FastAPI

from router import auth
from router import todo

app = FastAPI()
app.include_router(auth.router)
app.include_router(todo.router)
