from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from src.schemas.models import ModelQueryRequest, BenchmarkRequest
from src.services.model_provider import (
    call_llm,
    stream_llm,
    benchmark_models,
    get_provider_status
)

def get_providers_controller():
    try:
        return {
            "status": "success",
            "providers": get_provider_status()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider status check failed: {str(e)}")

def query_model_controller(request: ModelQueryRequest):
    try:
        messages = [
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.prompt}
        ]
        result = call_llm(
            provider=request.provider,
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            reasoning_effort=request.reasoning_effort
        )
        return {
            "status": "success",
            "prompt": request.prompt,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error ({request.provider}): {str(e)}")

def stream_model_controller(request: ModelQueryRequest):
    try:
        messages = [
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.prompt}
        ]
        generator = stream_llm(
            provider=request.provider,
            messages=messages,
            model=request.model,
            temperature=request.temperature
        )
        return StreamingResponse(generator, media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Streaming error ({request.provider}): {str(e)}")

def benchmark_controller(request: BenchmarkRequest):
    try:
        targets_dict = None
        if request.targets:
            targets_dict = [t.model_dump() for t in request.targets]
            
        results = benchmark_models(
            prompt=request.prompt,
            targets=targets_dict
        )
        return {
            "status": "success",
            "prompt": request.prompt,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark error: {str(e)}")
