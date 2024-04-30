from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from models import Courier
from schemas import CourierModel, CourierCreate, OrderModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

courier_router = APIRouter(
    prefix="/couriers",
    tags=['couriers']
)
session = Session(bind=engine)


@courier_router.get('/couriers')
async def list_all_couriers():
    couriers = session.query(Courier).all()
    return jsonable_encoder(couriers)


@courier_router.get('/courier/{id}')
async def get_courier_by_id(id: int):
    courier = session.query(Courier).filter(Courier.id == id).first()
    if not courier:
        return JSONResponse(status_code=404, content={"message": "courier not found"})

    active_order_info = None
    if courier.active_order:
        active_order_info = courier.active_order

    response = {
        "id": courier.id,
        "name": courier.name,
        "active_order": active_order_info,
        "avg_order_complete_time": courier.avg_order_complete_time,
        "avg_day_orders": courier.avg_day_orders
    }
    return jsonable_encoder(response)


@courier_router.post('/courier', status_code=status.HTTP_201_CREATED)
async def create_courier(user: CourierCreate):
    new_Courier = Courier(
        name=user.name,
        districts=user.districts,

    )
    session.add(new_Courier)
    session.commit()

    return new_Courier