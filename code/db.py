from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()
