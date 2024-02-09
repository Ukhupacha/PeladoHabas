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
    delivery_query = models.Peeling(**delivery.model_dump())
    db.add(delivery_query)
    db.commit()
    db.refresh(delivery_query)
    return delivery_query


@router.get("/", response_model=List[schemas.DeliveryOut])
async def get_deliveries(db:db_dependency, skip: int=0, limit: int =100):
    delivery_query = db.query(models.Peeling).offset(skip).limit(limit)
    deliveries = delivery_query.all()
    return deliveries


@router.get("/{id}", response_model=schemas.DeliveryOut)
async def get_delivery(id: int, db:db_dependency):
    delivery_query = db.query(models.Peeling).filter(models.Peeling.id == id).first()

    if not delivery_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"delivery with id: {id} does not exist")

    return delivery_query


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_delivery(id: int, db:db_dependency):
    
    delivery_query = db.query(models.Peeling).filter(models.Peeling.id == id)
    delivery_exist = delivery_query.first()

    if delivery_exist == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"delivery with id: {id} does not exist")
    
    delivery_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.DeliveryOut)
async def put_delivery(id: int, updated_delivery: schemas.DeliveryBase, db:db_dependency):
    delivery_query = db.query(models.Peeling).filter(models.Peeling.id == id)

    delivery_exist = delivery_query.first()
    if delivery_exist == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"delivery with id: {id} does not exist")
    
    delivery_query.update(updated_delivery.model_dump(), synchronize_session=False)
    db.commit()
    delivery_updated = delivery_query.first()
    return delivery_updated
