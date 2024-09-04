from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# create database engine
engine = create_engine('sqlite:///mygym.db')

# create session
Session = sessionmaker(bind=engine)
session = Session()

# %%
