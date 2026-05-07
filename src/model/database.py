from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import src.config as config

engine = create_engine(f"sqlite:///{config.DB_PATH}", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)