from fastapi import APIRouter
from src.schemas.multi_agent import DebateRequest, ThreeWayChatRequest
from src.controllers.multi_agent import debate_controller, three_way_controller

router = APIRouter(
    prefix="/multi-agent",
    tags=["Week 2 Day 1 - Multi-Agent Autonomous Conversations"]
)

@router.post("/debate")
def run_debate_endpoint(request: DebateRequest):
    """
    Autonomous 2-Agent Debate:
    Orchestrates an adversarial or collaborative back-and-forth dialogue
    between two AI personas across multiple rounds.
    """
    return debate_controller(request)

@router.post("/three-way")
def run_three_way_endpoint(request: ThreeWayChatRequest):
    """
    3-Way Round-Robin Conversation:
    Orchestrates a 3-agent group discussion (e.g. Alex vs Blake vs Pierre)
    feeding the cumulative dialogue transcript into every turn.
    """
    return three_way_controller(request)
