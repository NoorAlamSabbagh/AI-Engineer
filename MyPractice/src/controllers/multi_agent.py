from fastapi import HTTPException
from src.schemas.multi_agent import DebateRequest, ThreeWayChatRequest
from src.services.multi_agent import run_two_agent_debate, run_three_way_round_robin

def debate_controller(request: DebateRequest):
    try:
        a1_cfg = request.agent_1.model_dump() if request.agent_1 else None
        a2_cfg = request.agent_2.model_dump() if request.agent_2 else None

        result = run_two_agent_debate(
            topic=request.topic,
            rounds=request.rounds,
            agent_1_cfg=a1_cfg,
            agent_2_cfg=a2_cfg
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debate execution failed: {str(e)}")

def three_way_controller(request: ThreeWayChatRequest):
    try:
        a1_cfg = request.agent_1.model_dump() if request.agent_1 else None
        a2_cfg = request.agent_2.model_dump() if request.agent_2 else None
        a3_cfg = request.agent_3.model_dump() if request.agent_3 else None

        result = run_three_way_round_robin(
            topic=request.topic,
            rounds=request.rounds,
            agent_1_cfg=a1_cfg,
            agent_2_cfg=a2_cfg,
            agent_3_cfg=a3_cfg
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Three-way conversation failed: {str(e)}")
