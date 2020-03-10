import sqlalchemy as db
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, Text
from sqlalchemy import Column, VARCHAR, String, Integer


engine = db.create_engine('mysql://admin:IHOFpzwjHMVSNCOP32f1@138.201.92.24/covidmap')
connection = engine.connect()
metadata = db.MetaData()
metadata.bind = engine

Session = sessionmaker(bind=engine, autocommit=True, autoflush=True)
session = Session()

Base = declarative_base()

class Covid(Base):
    __tablename__ = 'data'
    country = db.Column(String(), primary_key=True)
    lastupdate = db.Column(String())
    confirmed = db.Column(Integer())
    deaths = db.Column(Integer())
    recovered = db.Column(Integer())
    latitude = db.Column(String())
    longitude = db.Column(String())


