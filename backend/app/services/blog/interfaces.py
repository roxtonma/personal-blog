from typing import List, Dict
from app.models.blog_model import BlogBase

class BlogRepository:
    async def list_blogs(self) -> List[BlogBase]:
        raise NotImplementedError

    async def create_blog(self, blog: BlogBase) -> BlogBase:
        raise NotImplementedError

    async def get_blog(self, blog_id: int) -> BlogBase:
        raise NotImplementedError
