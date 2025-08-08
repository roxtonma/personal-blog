from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.middleware import RateLimitMiddleware
from app.core.exceptions import (
    validation_exception_handler,
    blog_not_found_handler,
    gist_service_handler,
    authentication_handler,
    BlogNotFoundException,
    GistServiceException,
    AuthenticationException
)

from app.api.routes.blog import router as blog_router
from app.api.routes.auth import router as auth_router

def create_app() -> FastAPI:
    # Configure logging
    configure_logging()

    app = FastAPI(
        title="Roxton's Blog API",
        description="Personal blog API powered by GitHub Gists",
        version="1.0.0",
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/openapi.json"
    )

    # Middleware: CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware: Rate Limiting
    app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

    # Exception Handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(BlogNotFoundException, blog_not_found_handler)
    app.add_exception_handler(GistServiceException, gist_service_handler)
    app.add_exception_handler(AuthenticationException, authentication_handler)

    # Routers
    app.include_router(blog_router, prefix="/api/blog-posts", tags=["Blog"])
    app.include_router(auth_router, prefix="/api", tags=["Auth"])

    # Health Check
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "environment": settings.ENV}

    # Root Endpoint
    @app.get("/")
    async def root():
        return {"message": "Welcome to Roxton's Blog API"}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(settings.PORT), reload=settings.ENV == "development")
