
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Float, String, UniqueConstraint, \
                        ForeignKey


URI = 'postgresql://david:david@localhost:5432/green_hackathon'
engine = sqlalchemy.create_engine(URI)#, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Producer(Base):
    """Like 'EWZ Zuerich'"""
    __tablename__ = 'producer'
    __table_args__ = (UniqueConstraint('name', 'year'),)

    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)

    def __init__(self, name, year):
        self.name = name
        self.year = year


class Source(Base):
    """For things like 'Gaskraft'"""
    __tablename__ = 'source'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name


class Percent(Base):
    """the percents of the products are stored here"""
    __tablename__ = 'percent'
    producer_id = Column(Integer, ForeignKey(Producer.id), primary_key=True)
    source_id = Column(Integer, ForeignKey(Source.id), primary_key=True)
    percent = Column(Float)

    def __init__(self, producer, source, percent):
        self.producer_id = producer.id
        self.source_id = source.id
        self.percent = percent


class City(Base):
    __tablename__ = 'city'
    name = Column(String, primary_key=True)
    zip = Column(Integer, primary_key=True)
    producer_id = Column(Integer, ForeignKey(Producer.id))

    def __init__(self, city, zip, producer):
        self.name = city
        self.zip = zip
        self.producer_id = producer.id


Base.metadata.create_all(engine)
