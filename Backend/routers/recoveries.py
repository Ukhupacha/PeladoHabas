import models, schemas
from fastapi import Response, status, HTTPException, APIRouter
from database import db_dependency
from typing import List

router = APIRouter(
    prefix="/recoveries",
    tags=['Recoveries']
)

@router.post("/", response_model=schemas.RecoveryOut, status_code=status.HTTP_201_CREATED)
async def create_recovery(recovery: schemas.RecoveryBase, db:db_dependency):
    recovery_query = models.Peeling(**recovery.model_dump())
    db.add(recovery_query)
    db.commit()
    db.refresh(recovery_query)
    return recovery_query


@router.get("/", response_model=List[schemas.RecoveryOut])
async def get_recoveries(db:db_dependency, skip: int =0, limit: int=100):
    recovery_query = db.query(models.Peeling).offset(skip).limit(limit)
    recoveries = recovery_query.all()
    return recoveries


@router.get("/{id}", response_model=schemas.RecoveryOut)
async def get_delivery(id: int, db:db_dependency):
    recovery_query = db.query(models.Peeling).filter(models.Peeling.id == id).first()

    if not recovery_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"recovery with id: {id} does not exist")
    
    return recovery_query


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recovery(id: int, db:db_dependency):
    recovery_query = db.query(models.Peeling).filter(models.Peeling.id == id)
    recovery_exist = recovery_query.first()

    if recovery_exist == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"recovery with id: {id} does not exist")
    
    recovery_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.RecoveryOut)
async def put_recovery(id: int, updated_recovery: schemas.RecoveryBase, db:db_dependency):
    recovery_query = db.query(models.Peeling).filter(models.Peeling.id == id)

    recovery_exist = recovery_query.first()
    if recovery_exist == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"recovery with id: {id} does not exist")
    
    recovery_query.update(updated_recovery.model_dump(), synchronize_session=False)
    db.commit()
    recovery_updated = recovery_query.first()
    return recovery_updated