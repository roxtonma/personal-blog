from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    title: Optional[str] = None
    content: Optional[str] = None

class Blog(BlogBase):
    id: str
    date: datetime
    class Config:
        from_attributes = True
