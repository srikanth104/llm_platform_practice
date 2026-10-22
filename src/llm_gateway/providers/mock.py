import asyncio
from llm_gateway.providers.error import ErrorType, ProviderError

class ProviderRateLimitError(Exception):
    pass

class MockProvider:
        def __init__(self, name: str, delay: float,  fail_with_429: bool = False,):
                self.name = name
                self.delay = delay
                self.fail_with_429 = fail_with_429
                

        async def generate(self, prompt: str) -> str: 
                await asyncio.sleep(self.delay)

                if self.fail_with_429:
                        raise ProviderError(
                                ErrorType.RATE_LIMIT,
                                f"{self.name}: HTTP 429 Rate Limit Exceeded",)

                return f"{self.name}: Response to '{prompt}'"
                