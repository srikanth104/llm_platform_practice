from fastapi import FastAPI
from pydantic import BaseModel, Field
from llm_gateway.providers.mock import MockProvider
from llm_gateway.router import route_request


app = FastAPI(title="Enterprise LLM Gateway")

class ChatRequest(BaseModel):
    tenant_id: str
    prompt : str = Field(min_length=1)

@app.get("/health")
async def health():
     return {"status": "healthy"}

providers = {
         "openai": MockProvider("openai", 1.0),
        "gemini": MockProvider("gemini", 0.5),
        "anthropic": MockProvider("anthropic", 1.5),
}

@app.post("/v1/chat")
async def chat(request: ChatRequest):
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