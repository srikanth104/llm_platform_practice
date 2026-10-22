from fastapi import FastAPI
from pydantic import BaseModel, Field
from llm_gateway.providers.mock import MockProvider
from llm_gateway.router import route_request
from fastapi import HTTPException
from llm_gateway.router import AllProvidersFailedError
from llm_gateway.providers.error import ProviderError
from llm_gateway.rate_limiter import RateLimiter
from contextlib import asynccontextmanager
from redis.asyncio import Redis
from llm_gateway.redis_rate_limiter import RedisRateLimiter
from fastapi import Request


@asynccontextmanager
async def lifespan(app : FastAPI):
    redis = Redis.from_url(
        "redis://localhost:6379",
        decode_responses=True,
    )
    
    try:
        await redis.ping()
        app.state.rate_limiter = RedisRateLimiter(
            redis=redis,
            max_requests=3,
            window_seconds=60,
        )
        print("Redis connected")
        yield
    finally:
        await redis.aclose()
        print("Redis connection closed")


app = FastAPI(title="Enterprise LLM Gateway",
              lifespan=lifespan)



class ChatRequest(BaseModel):
    tenant_id: str
    prompt : str = Field(min_length=1)

@app.get("/health")
async def health():
     return {"status": "healthy"}

providers = {
    "openai": MockProvider(
        "openai", delay=0.2, fail_with_429=True
    ),
    "gemini": MockProvider(
        "gemini", delay=0.2, fail_with_429=True
    ),
}

@app.post("/v1/chat")
async def chat(request: ChatRequest, http_request: Request):
   
    if not await http_request.app.state.rate_limiter.allow(
        request.tenant_id):
        raise HTTPException(
            status_code=429,
            detail="Tenant rate limit exceeded",
        ) 
    
    try:
        answer = await route_request(
            request.prompt, 
            primary = providers["openai"],
            fallback = providers["gemini"]
        )

        return {
          "tenent_id": request.tenant_id,
          "provider":"routed",
          "answer":answer
        }
    except AllProvidersFailedError:
        raise HTTPException(
            status_code=503,
            detail="LLM providers temporarily unavailable",
        )

    except ProviderError:
        raise HTTPException(
            status_code=502,
            detail="LLM provider request rejected",
        )
