import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings
from app.core.exceptions import AuthenticationException

class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY if hasattr(settings, 'SECRET_KEY') else "change-this-secret-key"
        self.admin_password = settings.ADMIN_PASSWORD if hasattr(settings, 'ADMIN_PASSWORD') else "admin123"
        self.algorithm = "HS256"
        self.access_token_expire_hours = 24 * 7  # 1 week

    def create_access_token(self, subject: str, expires_delta: Optional[timedelta] = None) -> str:
        """Create a new access token"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=self.access_token_expire_hours)
        
        to_encode = {"exp": expire, "sub": subject, "iat": datetime.utcnow()}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> str:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None or username != "admin":
                raise AuthenticationException("Invalid token subject")
            return username
        except jwt.ExpiredSignatureError:
            raise AuthenticationException("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationException("Invalid token")

    def authenticate_admin(self, password: str) -> bool:
        """Authenticate admin with password"""
        return password == self.admin_password

    def login(self, password: str) -> str:
        """Login and return access token"""
        if not self.authenticate_admin(password):
            raise AuthenticationException("Invalid credentials")
        
        return self.create_access_token(subject="admin")

# Create a global instance
auth_service = AuthService()