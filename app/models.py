from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
import datetime


class USER(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)

    urls = relationship("URL", back_populates="user")


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String, nullable=False)
    shortened_url = Column(String, nullable=False, unique=True)
    creation_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    creator_id = Column(Integer, ForeignKey("users.id"))
    click_count = Column(Integer, default=0)
    expiration_timestamp = Column(DateTime)

    user = relationship("USER", back_populates="urls")
