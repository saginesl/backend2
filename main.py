from fastapi import FastAPI
from order_routes import order_router
from couriers_routes import courier_router
from database import init_db


app=FastAPI()


app.include_router(order_router)
app.include_router(courier_router)

@app.on_event("startup")
async def startup_event():
    await init_db()