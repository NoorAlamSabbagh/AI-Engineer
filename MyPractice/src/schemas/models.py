from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ModelQueryRequest(BaseModel):
    provider: str = Field(default="ollama", description="Provider to use: 'ollama', 'openai', 'groq'")
    model: Optional[str] = Field(default=None, description="Model identifier (e.g. 'llama3.2', 'gpt-4o-mini', 'qwen/qwen3.8-27b')")
    prompt: str = Field(..., description="User prompt to send to the model")
    system_prompt: Optional[str] = Field(
        default="You are an expert, helpful AI assistant.",
        description="System prompt defining persona and behavior"
    )
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=500, gt=0)
    reasoning_effort: Optional[str] = Field(
        default=None,
        description="Reasoning effort for reasoning models ('minimal', 'low', 'medium', 'high')"
    )

class ModelTarget(BaseModel):
    provider: str
    model: str

class BenchmarkRequest(BaseModel):
    prompt: str = Field(..., description="Prompt to benchmark across models")
    targets: Optional[List[ModelTarget]] = Field(
        default=None,
        description="List of target {provider, model} configs to compare. Defaults to comparing local Ollama with OpenAI."
    )
