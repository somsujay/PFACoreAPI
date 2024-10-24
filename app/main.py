from fastapi import FastAPI
from app.routes import users, pfaAPIRoute, items
from app.util.db.dbPoolManager import database

from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database pool
    await database.init_pool()
    yield
    # Cleanup code to close the pool
    await database.close_pool()

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(pfaAPIRoute.router)
app.include_router(items.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the PFACoreAPI (FastAPI)!"}
