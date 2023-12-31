from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

database_config = config['database']

# Constructing the URL_DATABASE using values from the configuration file
URL_DATABASE = f"mysql+pymysql://{database_config['username']}:{database_config['password']}@{database_config['host']}:{database_config['port']}/{database_config['database_name']}"

#URL_DATABASE = 'mysql+pymysql://root:1234@localhost:3306/new'
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
