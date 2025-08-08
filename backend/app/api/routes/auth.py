from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth_schema import LoginRequest, TokenResponse, AuthStatus
from app.services.auth.auth_service import auth_service
from app.core.dependencies import get_current_admin
from app.core.exceptions import AuthenticationException
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Authenticate admin user and return access token.
    """
    try:
        token = auth_service.login(request.password)
        logger.info("Admin login successful")
        return TokenResponse(
            token=token,
            token_type="bearer",
            expires_in=auth_service.access_token_expire_hours * 3600
        )
    except AuthenticationException as e:
        logger.warning(f"Failed login attempt: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

@router.get("/verify", response_model=AuthStatus)
async def verify_authentication(current_user: str = Depends(get_current_admin)):
    """
    Verify current authentication status.
    """
    return AuthStatus(authenticated=True, user=current_user)

@router.post("/logout")
async def logout():
    """
    Logout endpoint (token invalidation happens client-side).
    """
    return {"message": "Logged out successfully"}
