from redis.asyncio import Redis
RATE_LIMIT_SCRIPT = """
local count = redis.call('INCR', KEYS[1])

if count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end

return count <= tonumber(ARGV[2])
"""

class RedisRateLimiter:
    def __init__(
        self,
        redis: Redis,
        max_requests: int = 3,
        window_seconds: int = 60):
        self.redis = redis
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    async def allow(self, tenant_id:str) -> bool:
         key = f"rate_limit:{tenant_id}"
         
         allowed = await self.redis.eval(
             RATE_LIMIT_SCRIPT, 
             1,
             key, 
             self.window_seconds,
             self.max_requests
         )
         
         return bool(allowed)
        