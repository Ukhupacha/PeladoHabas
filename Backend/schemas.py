
from pydantic import BaseModel
from datetime import datetime, date

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


class RecoveryBase(BaseModel):
    return_date : date
    total : float
    peeled_whole : float
    peeled_split : float
    green : float
    soles : float
    comments : str


class RecoveryOut(RecoveryBase):
    kilos: float
    worker_id: int
    id: int
    delivery_date: datetime
    class Config:
        from_attributes = True