from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import config

engine = create_engine(config.get_db_uri(), echo=True)
metadata = MetaData()
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
