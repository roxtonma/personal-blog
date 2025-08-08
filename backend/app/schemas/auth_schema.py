from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    password: str = Field(..., min_length=1, description="Admin password")

class TokenResponse(BaseModel):
    token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(default=604800, description="Token expiration in seconds (1 week)")

class AuthStatus(BaseModel):
    authenticated: bool = Field(..., description="Whether the user is authenticated")
    user: str = Field(..., description="Username of authenticated user")
