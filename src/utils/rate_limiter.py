import asyncio
from datetime import datetime, timedelta
from collections import deque
import logging
from typing import List

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.window_size = timedelta(minutes=1)
        self.calls = deque()
    
    async def wait_if_needed(self):
        """Wait if we've exceeded our rate limit"""
        now = datetime.utcnow()
        
        # Remove old calls outside the window
        while self.calls and self.calls[0] < now - self.window_size:
            self.calls.popleft()
        
        # If we're at the limit, wait until the oldest call expires
        if len(self.calls) >= self.calls_per_minute:
            wait_time = (self.calls[0] + self.window_size - now).total_seconds()
            if wait_time > 0:
                logger.info(f"Rate limit reached. Waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
        
        # Add the current call
        self.calls.append(now)