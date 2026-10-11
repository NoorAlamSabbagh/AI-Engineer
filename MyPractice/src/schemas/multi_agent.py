from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AgentConfig(BaseModel):
    name: str = Field(..., description="Name of the agent (e.g. 'Alex', 'Blake', 'Suresh')")
    provider: str = Field(default="ollama", description="'ollama', 'openai', or 'groq'")
    model: Optional[str] = Field(default=None, description="Model to use (defaults to provider's best option)")
    personality: str = Field(..., description="System instructions shaping agent's behavior, tone, or perspective")

class DebateRequest(BaseModel):
    topic: str = Field(..., description="Debate topic or opening premise")
    rounds: int = Field(default=3, ge=1, le=10, description="Number of back-and-forth turns")
    agent_1: Optional[AgentConfig] = Field(
        default=None,
        description="Configuration for the first agent (default: Sarcastic Challenger on OpenAI)"
    )
    agent_2: Optional[AgentConfig] = Field(
        default=None,
        description="Configuration for the second agent (default: Diplomatic Peacemaker on local Ollama)"
    )

class ThreeWayChatRequest(BaseModel):
    topic: str = Field(..., description="Discussion subject")
    rounds: int = Field(default=2, ge=1, le=5, description="Number of complete round-robin cycles (each cycle is 3 turns)")
    agent_1: Optional[AgentConfig] = Field(
        default=None,
        description="First participant (default: Alex - Provocateur & Skeptic)"
    )
    agent_2: Optional[AgentConfig] = Field(
        default=None,
        description="Second participant (default: Blake - Pragmatic Problem Solver)"
    )
    agent_3: Optional[AgentConfig] = Field(
        default=None,
        description="Third participant (default: Charlie - Creative Visionary & Philosopher)"
    )
