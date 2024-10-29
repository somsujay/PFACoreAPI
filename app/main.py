from fastapi import FastAPI
from app.routes import users, pfa_api_route, items
from app.util.db.dbPoolManager import database
from contextlib import asynccontextmanager
import uvicorn

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
app.include_router(pfa_api_route.router)
app.include_router(items.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the PFACoreAPI (FastAPI)!"}

if __name__ == "__main__":
    # Start the Uvicorn server with specific settings
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)