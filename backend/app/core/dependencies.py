
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth.auth_service import auth_service
from app.core.exceptions import AuthenticationException
from typing import Optional

security = HTTPBearer()

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to verify admin authentication.
    Returns the admin username if authentication is successful.
    """
    try:
        username = auth_service.verify_token(credentials.credentials)
        return username
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

async def optional_admin(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> Optional[str]:
    """
    Optional admin authentication - returns admin username if authenticated, None otherwise.
    Useful for endpoints that have different behavior for admin vs public access.
    """
    if not credentials:
        return None
    
    try:
        return auth_service.verify_token(credentials.credentials)
    except AuthenticationException:
        return None