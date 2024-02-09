
from pydantic import BaseModel
from datetime import datetime

class WorkerBase(BaseModel):    
    last_name: str
    first_name: str    
    DNI: str
    sector: str
    address: str
    GPS: str    
    phone: str
    genre: bool
    photo: str


class WorkerOut(WorkerBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


class DeliveryBase(BaseModel):
    kilos: float
    worker_id: int


class DeliveryOut(DeliveryBase):
    id: int
    delivery_date: datetime
    class Config:
        from_attributes = True






