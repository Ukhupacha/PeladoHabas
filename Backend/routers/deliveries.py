import models, schemas
from fastapi import Response, status, HTTPException, APIRouter
from database import db_dependency
from typing import List

router = APIRouter(
    prefix="/deliveries",
    tags=['Deliveries']
)

@router.post("/", response_model=schemas.DeliveryOut, status_code=status.HTTP_201_CREATED)
async def create_delivery(delivery: schemas.DeliveryBase, db: db_dependency):
    db_delivery = models.Delivery(**delivery.dict())
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery