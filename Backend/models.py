from database import Base
from sqlalchemy import Column, Integer, String, Boolean, NUMERIC, REAL
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
    

class Delivery(Base):
    __tablename__ = 'deliveries'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    delivery_date = Column(TIMESTAMP(timezone=True),
                           nullable=False, server_default=text('now()'))
    kilos = Column(REAL, nullable=False)
    reception_date = Column(TIMESTAMP(timezone=True))
    total = Column(REAL)
    green = Column(REAL)
    pealed_whole = Column(REAL)
    pealed_split = Column(REAL)
    soles = Column(NUMERIC)
    paid = Column(Boolean, server_default='False', nullable=False)
    comments = Column(String)
    pay_date = Column(TIMESTAMP(timezone=True))    