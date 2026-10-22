import asyncio
from llm_gateway.providers.base import LLMProvider
from llm_gateway.providers.error import (
    ErrorType,
    ProviderError,
    should_fallback,
)

class AllProvidersFailedError(Exception):
    pass

async def route_request(
        prompt: str, 
        primary : LLMProvider, 
        fallback : LLMProvider
) -> str : 
    try:
        async with asyncio.timeout(3):
            try:
                async with asyncio.timeout(2):
                    return await primary.generate(prompt)
            except TimeoutError : 
                error_type = ErrorType.TIMEOUT
            except ProviderError as exc:
                error_type = exc.error_type

            if not should_fallback(error_type):
                raise ProviderError(
                    error_type,
                    "Provider error does not permit fallback",
                )

            try:
                return await fallback.generate(prompt)
            except ProviderError as exc:
                raise AllProvidersFailedError(
                    "Both providers are unavailable"
                ) from exc
    except TimeoutError as exc:
        raise AllProvidersFailedError(
            "Gateway deadline exceeded"
        ) from exc
    