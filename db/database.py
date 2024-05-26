
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

ENGINE = create_engine('postgresql://postgres:diyor@localhost/fast_database', echo=True)

Base = declarative_base()
Session = sessionmaker()
