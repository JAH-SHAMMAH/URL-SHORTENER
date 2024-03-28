from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:guarantee@localhost:5432/Url_db"
SQLALCHEMY_DATABASE_URL = "postgresql://uwphtvzb:ragNbCxzhebQ5hKpTcI_lbtZl9Bu5KTU@rain.db.elephantsql.com:5432/uwphtvzb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
