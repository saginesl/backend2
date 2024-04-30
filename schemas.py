from pydantic import BaseModel
from typing import Optional, List

class CourierModel(BaseModel):
    id: Optional[int]
    name: str
    avg_order_complete_time: int
    avg_day_orders: int
    active_order_id: Optional[int]
    active_order: Optional[dict]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "ivanov", "avg_order_complete_time": 1505, "avg_day_orders": 25

            }
        }


class OrderModel(BaseModel):
    id: Optional[int]
    name: str
    district: str
    status: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 150, "name": "delivery", "district": "center", "status": 1,
                "assigned_courier_id": 12
            }
        }


class CourierCreate(BaseModel):
    name: str
    districts: List[str]


class OrderCreate(BaseModel):
    name: str
    district: str