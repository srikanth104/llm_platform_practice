import asyncio
from llm_gateway.providers.base import LLMProvider

async def route_request(
        prompt: str, 
        primary : LLMProvider, 
        fallback : LLMProvider
) -> str : 
    async with asyncio.timeout(3):
        try:
            async with asyncio.timeout(2):
                return await primary.generate(prompt)
        except TimeoutError:
            print("Primary timed out. Trying fallback.")
            return await fallback.generate(prompt)