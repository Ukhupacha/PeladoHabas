import models, schemas
from fastapi import Response, status, HTTPException, APIRouter
from database import db_dependency
from typing import List

router = APIRouter(
    prefix="/payments",
    tags=['Payments']
)

@router.post("/", response_model=schemas.PaymentOut, status_code=status.HTTP_201_CREATED)
async def create_payment(payment: schemas.PaymentBase, db:db_dependency):
    payment_query = models.Peeling(**payment.model_dump())
    db.add(payment_query)
    db.commit()
    db.refresh(payment_query)
    return payment_query


@router.get("/", response_model=List[schemas.PaymentOut])
async def get_payments(db:db_dependency, skip: int =0, limit: int=100):
    payment_query = db.query(models.Peeling).offset(skip).limit(limit)
    payments = payment_query.all()
    return payments


@router.get("/{id}", response_model=schemas.PaymentOut)
async def get_payment(id: int, db:db_dependency):
    payment_query = db.query(models.Peeling).filter(models.Peeling.id == id).first()

    if not payment_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"payment with id: {id} does not exist")
    
    return payment_query


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(id: int, db:db_dependency):
    payment_query = db.query(models.Peeling).filter(models.Peeling.id == id)
    payment_exist = payment_query.first()

    if payment_exist == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"payment with id: {id} does not exist")
    
    payment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PaymentOut)
async def put_payment(id: int, updated_payment: schemas.PaymentBase, db:db_dependency):
    payment_query = db.query(models.Peeling).filter(models.Peeling.id == id)

    payment_exist = payment_query.first()
    if payment_exist == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"payment with id: {id} does not exist")
    
    payment_query.update(updated_payment.model_dump(), synchronize_session=False)
    db.commit()
    payment_updated = payment_query.first()
    return payment_updated