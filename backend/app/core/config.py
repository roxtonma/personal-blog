import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    ENV: str = 'development'
    GITHUB_TOKEN: Optional[str] = None
    GIST_ID: Optional[str] = None
    GIST_IDS: Optional[str] = None
    PORT: str = '8000'
    FRONTEND_URL: str = 'http://localhost:5173'
    DATABASE_URL: str = 'sqlite+aiosqlite:///./blog.db'
    
    # Authentication settings
    SECRET_KEY: str = 'your-secret-key-change-this-in-production'
    ADMIN_PASSWORD: str = 'admin123'  # Change this!
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

    def validate(self):
        if not self.GITHUB_TOKEN:
            print("Warning: GITHUB_TOKEN environment variable is not set")
        if not self.GIST_ID:
            print("Warning: GIST_ID environment variable is not set")
        if self.ADMIN_PASSWORD == 'admin123':
            print("Warning: Using default admin password. Please change ADMIN_PASSWORD in environment variables.")
        if self.SECRET_KEY == 'your-secret-key-change-this-in-production':
            print("Warning: Using default secret key. Please change SECRET_KEY in environment variables.")

settings = Settings()
settings.validate()
