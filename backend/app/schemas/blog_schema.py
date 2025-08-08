from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class BlogCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = Field(default_factory=list)
    media: Optional[List[str]] = Field(default_factory=list)
    
    @validator('tags')
    def validate_tags(cls, v):
        if v and len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return v

class BlogResponse(BaseModel):
    id: str
    title: str
    content: str
    summary: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    media: Optional[List[str]] = Field(default_factory=list)
    date: datetime
    slug: Optional[str] = None
    
    class Config:
        from_attributes = True

class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    media: Optional[List[str]] = None
