import asyncio
import time 
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, max_requests:int, window_seconds:int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)
        self.lock = asyncio.Lock()
    
    async def allow(self, tenant_id:str) -> bool:
        async with self.lock:
            now = time.monotonic()
            timestamps = self.requests[tenant_id]
            
            while timestamps and now-timestamps[0] >= self.window_seconds:
                timestamps.popleft()
            if(len(timestamps)) >= self.max_requests:
                return False
            
            timestamps.append(now)
            return True
        