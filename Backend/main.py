from fastapi import FastAPI, HTTPException, Depends, status, Response
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from database import engine, get_db
import models
import schemas
import argparse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers import workers, deliveries, recoveries

app = FastAPI()

origins = [
    "http://localhost:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(bind=engine)


app.include_router(workers.router)
app.include_router(deliveries.router)
app.include_router(recoveries.router)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Attendance app')
    parser.add_argument('-a', '--address', help='Host address', default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int, help='Host port', default=8000)

    args = parser.parse_args()
    uvicorn.run(app, host=args.address, port=args.port)
