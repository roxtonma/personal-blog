import httpx
import json
from datetime import datetime
from typing import List, Optional
import logging

from app.services.blog.interfaces import BlogRepository
from app.models.blog_model import Blog
from app.core.config import settings
from app.schemas.blog_schema import BlogCreate, BlogUpdate

logger = logging.getLogger(__name__)

class GistBlogService(BlogRepository):
    def __init__(self):
        self.api_url = f"https://api.github.com/gists/{settings.GIST_ID}"
        self.headers = {
            "Authorization": f"token {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        self.filename = "blog_data.json"

    async def _fetch_data(self) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(self.api_url, headers=self.headers)
                res.raise_for_status()
                
                if self.filename not in res.json()["files"]:
                    return {}
                    
                file_content = res.json()["files"][self.filename]["content"]
                return json.loads(file_content)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return {}
                raise

    async def _write_data(self, data: dict):
        async with httpx.AsyncClient() as client:
            updated_content = json.dumps(data, indent=2)
            await client.patch(self.api_url, headers=self.headers, json={
                "files": {
                    self.filename: {"content": updated_content}
                }
            })

    async def list_blogs(self) -> List[Blog]:
        try:
            data = await self._fetch_data()
            return [Blog(**v) for v in data.values()]
        except Exception as e:
            logger.error(f"Error fetching blogs: {str(e)}")
            raise

    async def get_blog(self, blog_id: int) -> Optional[Blog]:
        try:
            data = await self._fetch_data()
            blog_data = data.get(str(blog_id))
            if not blog_data:
                return None
            return Blog(**blog_data)
        except Exception as e:
            logger.error(f"Error fetching blog {blog_id}: {str(e)}")
            raise

    async def create_blog(self, blog: BlogCreate) -> Blog:
        try:
            data = await self._fetch_data()
            new_id = str(max([int(i) for i in data.keys()] + [0]) + 1)
            now_str = datetime.now().isoformat()

            blog_data = blog.model_dump()
            blog_data.update({"id": new_id, "date": now_str})
            data[new_id] = blog_data

            await self._write_data(data)
            logger.info(f"Created blog post with ID: {new_id}")
            return Blog(**blog_data)
        except Exception as e:
            logger.error(f"Error creating blog: {str(e)}")
            raise

    async def update_blog(self, blog_id: int, blog_update: BlogUpdate) -> Optional[Blog]:
        try:
            data = await self._fetch_data()
            blog_key = str(blog_id)
            
            if blog_key not in data:
                return None
            
            # Update only the fields that are provided
            existing_blog = data[blog_key]
            update_data = blog_update.model_dump(exclude_unset=True)
            
            for key, value in update_data.items():
                if value is not None:
                    existing_blog[key] = value
            
            # Update the modification date
            existing_blog["date"] = datetime.now().isoformat()
            
            await self._write_data(data)
            logger.info(f"Updated blog post with ID: {blog_id}")
            return Blog(**existing_blog)
        except Exception as e:
            logger.error(f"Error updating blog {blog_id}: {str(e)}")
            raise

    async def delete_blog(self, blog_id: int) -> bool:
        try:
            data = await self._fetch_data()
            blog_key = str(blog_id)
            
            if blog_key not in data:
                return False
            
            del data[blog_key]
            await self._write_data(data)
            logger.info(f"Deleted blog post with ID: {blog_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting blog {blog_id}: {str(e)}")
            raise
