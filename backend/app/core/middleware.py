from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
import time
import asyncio

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute=60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_times = {}
        
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean up old requests
        self.request_times = {ip: times for ip, times in self.request_times.items() 
                             if current_time - times[-1] < 60}
        
        # Initialize for new client
        if client_ip not in self.request_times:
            self.request_times[client_ip] = []
        
        # Check rate limit
        if len(self.request_times[client_ip]) >= self.requests_per_minute:
            return Response(
                content="Rate limit exceeded",
                status_code=429
            )
        
        # Add request time
        self.request_times[client_ip].append(current_time)
        
        # Process request
        response = await call_next(request)
        return response