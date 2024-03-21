from pydantic import BaseModel, HttpUrl
from datetime import datetime


class LoginUser(BaseModel):
    username: str
    email: str


class URLRequest(BaseModel):
    url: str


class LongURLRequest(BaseModel):
    long_url: str


class ShortenedURL(BaseModel):
    shortened_url: str


class LinkHistory(BaseModel):
    original_url: str
    shortened_url: str
    created_at: datetime
    clicks: int = 0
