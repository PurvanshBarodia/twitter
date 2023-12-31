from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL_DATABASE = 'mysql+pymysql://root:1234@localhost:3306/new'
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
