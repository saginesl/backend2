from fastapi import APIRouter, Depends, status, HTTPException
from models import Courier, Order
from schemas import OrderModel, CourierModel, OrderCreate
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

order_router = APIRouter(
    prefix="/orders",
    tags=['orders']
)
session = Session(bind=engine)


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
    courier = session.query(Courier).filter(Courier.active_order == None,
                                            Courier.districts.contains(order_data.district)).first()

    if not courier:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No available courier in the specified district")

    new_order = Order(
        name=order_data.name,
        district=order_data.district,
        courier_id=courier.id,
        status=1
    )

    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    return {
        "order_id": new_order.id,
        "courier_id": courier.id
    }


@order_router.get('/order/{id}')
async def get_order_by_id(id: int):
    order = session.query(Order).filter(Order.id == id).first()
    if not order:
        return JSONResponse(status_code=404, content={"message": "Order not found"})
    return {
        "courier_id": order.courier_id,
        "status": order.status,
    }


@order_router.post('/order/{id}', status_code=status.HTTP_201_CREATED)
async def complete_order(id: int):
    order = session.query(Order).filter(Order.id == id).first()
    if not order:
        return JSONResponse(status_code=404, content={"message": "Order not found"})
    if order.status == 2:
        return JSONResponse(status_code=201, content={"message": "Order completed"})

    courier = session.query(Courier).filter(Courier.id == order.courier_id).first()
    if courier:
        courier.active_order = []
        order.status = 2
        session.commit()

        return JSONResponse(status_code=201, content={"message": "Order completed"})
    else:
        return JSONResponse(status_code=404, content={"message": "Courier not found for the order"})