import os
import time
import requests
from typing import Generator, Dict, Any, List, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Default model per provider
DEFAULT_MODELS = {
    "ollama": "llama3.2",
    "openai": "gpt-4o-mini",
    "groq": "qwen/qwen3.8-27b"
}

def get_client_and_model(provider: str, requested_model: Optional[str] = None):
    """
    Returns an instantiated OpenAI client pointed to the right base_url,
    along with the resolved model name.
    """
    provider = provider.lower().strip()
    
    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        client = OpenAI(base_url=base_url, api_key="ollama")
        model = requested_model or DEFAULT_MODELS["ollama"]
        return client, model
        
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment.")
        client = OpenAI(api_key=api_key)
        model = requested_model or DEFAULT_MODELS["openai"]
        return client, model
        
    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in environment.")
        client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
        model = requested_model or DEFAULT_MODELS["groq"]
        return client, model
        
    else:
        raise ValueError(f"Unsupported provider: '{provider}'. Supported: 'ollama', 'openai', 'groq'.")

def get_installed_ollama_models() -> List[str]:
    """Queries the local Ollama daemon for installed models."""
    try:
        res = requests.get("http://localhost:11434/api/tags", timeout=2)
        if res.status_code == 200:
            data = res.json()
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        pass
    return []

def get_provider_status() -> Dict[str, Any]:
    """Returns the operational status of each provider."""
    ollama_models = get_installed_ollama_models()
    return {
        "ollama": {
            "available": len(ollama_models) > 0,
            "type": "local",
            "endpoint": "http://localhost:11434/v1",
            "installed_models": ollama_models,
            "default_model": DEFAULT_MODELS["ollama"]
        },
        "openai": {
            "available": bool(os.getenv("OPENAI_API_KEY")),
            "type": "cloud",
            "default_model": DEFAULT_MODELS["openai"]
        },
        "groq": {
            "available": bool(os.getenv("GROQ_API_KEY")),
            "type": "cloud",
            "default_model": DEFAULT_MODELS["groq"]
        }
    }

def call_llm(
    provider: str,
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: Optional[float] = 0.7,
    max_tokens: Optional[int] = 500,
    reasoning_effort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes a standard chat completion against any supported provider.
    Measures duration and extracts token usage. Supports reasoning_effort for reasoning models.
    """
    client, resolved_model = get_client_and_model(provider, model)
    
    start_time = time.time()
    call_kwargs: Dict[str, Any] = {
        "model": resolved_model,
        "messages": messages
    }
    
    # Reasoning models (e.g. gpt-5-nano, o1, o3) use reasoning_effort and do not allow custom temperature
    is_reasoning = reasoning_effort is not None or any(p in resolved_model.lower() for p in ["gpt-5", "o1", "o3"])
    if is_reasoning:
        if reasoning_effort:
            call_kwargs["reasoning_effort"] = reasoning_effort
    else:
        if temperature is not None:
            call_kwargs["temperature"] = temperature
        if max_tokens is not None:
            call_kwargs["max_tokens"] = max_tokens

    response = client.chat.completions.create(**call_kwargs)
    duration_sec = round(time.time() - start_time, 3)
    
    content = response.choices[0].message.content or ""
    
    usage_info = {
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None
    }
    if hasattr(response, "usage") and response.usage:
        usage_info["prompt_tokens"] = response.usage.prompt_tokens
        usage_info["completion_tokens"] = response.usage.completion_tokens
        usage_info["total_tokens"] = response.usage.total_tokens

    return {
        "provider": provider,
        "model": resolved_model,
        "content": content,
        "duration_seconds": duration_sec,
        "usage": usage_info
    }

def stream_llm(
    provider: str,
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7
) -> Generator[str, None, None]:
    """
    Yields content delta tokens in real-time from the chosen provider.
    """
    client, resolved_model = get_client_and_model(provider, model)
    stream = client.chat.completions.create(
        model=resolved_model,
        messages=messages,
        temperature=temperature,
        stream=True
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def benchmark_models(prompt: str, targets: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, Any]]:
    """
    Runs the same prompt across multiple targets (e.g. Local Ollama vs Cloud OpenAI)
    and collects side-by-side performance statistics.
    """
    if not targets:
        targets = [
            {"provider": "ollama", "model": DEFAULT_MODELS["ollama"]},
            {"provider": "openai", "model": DEFAULT_MODELS["openai"]}
        ]
        
    messages = [
        {"role": "system", "content": "You are a concise, sharp AI assistant. Answer directly and precisely."},
        {"role": "user", "content": prompt}
    ]
    
    results = []
    for target in targets:
        provider = target.get("provider", "ollama")
        model = target.get("model")
        try:
            res = call_llm(provider=provider, messages=messages, model=model)
            results.append({
                "target": f"{provider} ({res['model']})",
                "status": "success",
                "duration_seconds": res["duration_seconds"],
                "tokens": res["usage"]["total_tokens"],
                "response": res["content"]
            })
        except Exception as e:
            results.append({
                "target": f"{provider} ({model})",
                "status": "error",
                "error": str(e)
            })
            
    return results
