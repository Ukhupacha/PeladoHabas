import models, schemas
from fastapi import Response, status, HTTPException, APIRouter
from database import db_dependency
from typing import List


router = APIRouter(
    prefix="/workers",
    tags=['Posts']
)

@router.post("/", response_model=schemas.WorkerOut, status_code=status.HTTP_201_CREATED)
async def create_worker(worker: schemas.WorkerBase, db: db_dependency):
    db_worker = models.Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


@router.get("/", response_model=List[schemas.WorkerOut])
async def get_workers(db:db_dependency, skip: int = 0 , limit: int = 100):
    workers_query = db.query(models.Worker).offset(skip).limit(limit)
    workers = workers_query.all()
    return workers


@router.get("/{id}", response_model=schemas.WorkerOut)
async def get_worker(id: int, db:db_dependency):

    worker_query = db.query(models.Worker).filter(models.Worker.id == id).first()
    
    if not worker_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"worker with id : {id} was not found")
    return worker_query
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker(id: int, db:db_dependency):

    worker_query = db.query(models.Worker).filter(models.Worker.id == id)
    if worker_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"worker with id: {id} does not exist")
    
    worker_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.WorkerOut)
async def update_worker(id: int, updated_worker: schemas.WorkerBase, db:db_dependency):
    worker_query = db.query(models.Worker).filter(models.Worker.id == id)
    
    worker = worker_query.first()
    if worker == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"worker with id: {id} does not exist")
    
    worker_query.update(**updated_worker.dict(), synchronize_session=False)
    db.commit()
    update = worker_query.first()
    return update




