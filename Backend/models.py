from database import Base
from sqlalchemy import Column, Integer, String, Boolean, NUMERIC, REAL, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Worker(Base):
    __tablename__ = 'workers'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    DNI = Column(String, nullable=False, unique=True)
    sector = Column(String, nullable=False)
    address = Column(String, nullable=False)
    GPS = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    genre = Column(Boolean, server_default='TRUE', nullable=False)
    photo = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    

class Peeling(Base):
    __tablename__ = 'peelings'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    delivery_date = Column(TIMESTAMP(timezone=True),
                           nullable=False, server_default=text('now()'))
    worker_id = Column(Integer, ForeignKey("workers.id"))
    kilos = Column(REAL, nullable=False)
    return_date = Column(Date)
    total = Column(REAL, default=0)    
    peeled_whole = Column(REAL, default=0)
    peeled_split = Column(REAL, default=0)
    green = Column(REAL, default=0)
    soles = Column(NUMERIC, default=0)
    comments = Column(String)
    paid = Column(Boolean, server_default='False', nullable=False)
    payment_date = Column(Date)
    
