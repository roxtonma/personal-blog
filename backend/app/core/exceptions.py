from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation exceptions and return a structured error response.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

class BlogNotFoundException(Exception):
    """Exception raised when a blog post is not found."""
    pass

async def blog_not_found_handler(request: Request, exc: BlogNotFoundException):
    """
    Handle blog not found exceptions.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Blog post not found"},
    )

class GistServiceException(Exception):
    """Exception raised when there's an issue with the Gist service."""
    pass

async def gist_service_handler(request: Request, exc: GistServiceException):
    """
    Handle Gist service exceptions.
    """
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "GitHub Gist service unavailable", "message": str(exc)},
    )

class AuthenticationException(Exception):
    """Exception raised when authentication fails."""
    pass

async def authentication_handler(request: Request, exc: AuthenticationException):
    """
    Handle authentication exceptions.
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Authentication failed", "message": str(exc)},
    )
