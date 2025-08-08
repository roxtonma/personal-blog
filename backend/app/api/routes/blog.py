from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict

from app.schemas.blog_schema import BlogCreate, BlogResponse, BlogUpdate
from app.services.blog.gist_service import GistBlogService
from app.models.blog_model import Blog
from app.core.dependencies import get_current_admin, optional_admin

router = APIRouter()
blog_service = GistBlogService()

@router.get("/", response_model=Dict[str, BlogResponse])
async def get_blogs():
    """
    Get all blog posts. Public endpoint - no authentication required.
    """
    try:
        blogs = await blog_service.list_blogs()
        return {str(blog.id): blog for blog in blogs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch blogs: {str(e)}")

@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: int):
    """
    Get a specific blog post. Public endpoint - no authentication required.
    """
    try:
        blog = await blog_service.get_blog(blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return blog
    except KeyError:
        raise HTTPException(status_code=404, detail="Blog not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/", response_model=BlogResponse)
async def create_blog(
    blog: BlogCreate, 
    current_user: str = Depends(get_current_admin)
):
    """
    Create a new blog post. Requires admin authentication.
    """
    try:
        return await blog_service.create_blog(blog)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create blog: {str(e)}")

@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int,
    blog_update: BlogUpdate,
    current_user: str = Depends(get_current_admin)
):
    """
    Update an existing blog post. Requires admin authentication.
    """
    try:
        # You'll need to implement this method in your GistBlogService
        updated_blog = await blog_service.update_blog(blog_id, blog_update)
        if not updated_blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return updated_blog
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update blog: {str(e)}")

@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: int,
    current_user: str = Depends(get_current_admin)
):
    """
    Delete a blog post. Requires admin authentication.
    """
    try:
        # You'll need to implement this method in your GistBlogService
        success = await blog_service.delete_blog(blog_id)
        if not success:
            raise HTTPException(status_code=404, detail="Blog not found")
        return {"message": "Blog deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete blog: {str(e)}")
