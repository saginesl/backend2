import uvicorn
from fastapi import FastAPI
from books import router
from database import create_async_tables, init_db

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await init_db()
    await create_async_tables()