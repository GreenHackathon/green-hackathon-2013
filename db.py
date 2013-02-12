
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, Float, String, UniqueConstraint


URI = 'postgresql://scott:tiger@localhost:5432/green_hackathon'
engine = sqlalchemy.create_engine(URI, echo=True)

class Producer(Base):
    """Like 'EWZ Zuerich'"""
    __tablename__ = 'producer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)

    UniqueConstraint(name, year)

    def __init__(self, name, year):
        self.name = name
        self.year = year


class Product(Base):
    """For things like 'Gaskraft'"""
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Percent(Base):
    producer_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    percent = Column(Integer)

    def __init__(self, name, year):
        self.product_id = name
        self.year = year
