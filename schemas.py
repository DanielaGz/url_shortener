from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class URLCreate(BaseModel):
    long_url: HttpUrl
    createdAt: Optional[datetime] = None 

class URLResponse(BaseModel):
    short_url: str
    long_url: str
