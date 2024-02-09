import models, schemas
from fastapi import Response, status, HTTPException, APIRouter
from database import db_dependency
from typing import List

router = APIRouter(
    prefix="/peelings",
    tags=['Peelings']
)

@router.post("/", response_model=schemas.DeliveryOut, status_code=status.HTTP_201_CREATED)
async def create_peeling(peeling: schemas.DeliveryBase, db: db_dependency):
    peeling_query = models.Delivery(**peeling.model_dump())
    db.add(peeling_query)
    db.commit()
    db.refresh(peeling_query)
    return peeling_query