import asyncio

class MockProvider:
        def __init__(self, name: str, delay: float):
                self.name = name
                self.delay = delay

        async def generate(self, prompt: str) -> str: 
                await asyncio.sleep(self.delay)
                return f"{self.name}: Response to '{prompt}'"
                