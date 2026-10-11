from typing import List, Dict, Any, Optional
from src.services.model_provider import call_llm

def run_two_agent_debate(
    topic: str,
    rounds: int = 3,
    agent_1_cfg: Optional[Dict[str, Any]] = None,
    agent_2_cfg: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Executes an autonomous back-and-forth dialogue between two LLM agents.
    Demonstrates the Week 2 Day 1 multi-bot conversation pattern.
    """
    # 1. Defaults if not provided
    a1 = agent_1_cfg or {
        "name": "Alex (Skeptic)",
        "provider": "openai",
        "model": "gpt-4o-mini",
        "personality": (
            "You are Alex, a sharp, skeptical, and argumentative tech thinker. "
            "You challenge conventional wisdom, poke holes in optimistic claims, and speak concisely."
        )
    }
    
    a2 = agent_2_cfg or {
        "name": "Blake (Diplomat)",
        "provider": "ollama",
        "model": "llama3.2",
        "personality": (
            "You are Blake, a constructive, optimistic, and diplomatic engineer. "
            "You find common ground, highlight practical solutions, and defuse tensions calmly."
        )
    }

    transcript: List[Dict[str, str]] = []
    
    # 2. Opening statement from Agent 1
    opening_messages = [
        {"role": "system", "content": a1["personality"]},
        {"role": "user", "content": f"Opening topic for debate: '{topic}'. Give your initial sharp take in 2-3 sentences."}
    ]
    res1 = call_llm(provider=a1["provider"], model=a1.get("model"), messages=opening_messages)
    transcript.append({
        "speaker": a1["name"],
        "provider": a1["provider"],
        "model": res1["model"],
        "message": res1["content"]
    })

    # 3. Multi-round exchange
    for round_idx in range(1, rounds + 1):
        # --- AGENT 2 TURN ---
        formatted_history = "\n".join([f"{t['speaker']}: {t['message']}" for t in transcript])
        a2_messages = [
            {"role": "system", "content": a2["personality"]},
            {
                "role": "user",
                "content": (
                    f"The debate topic is: '{topic}'.\n"
                    f"The dialogue so far:\n{formatted_history}\n\n"
                    f"Respond directly to {a1['name']}'s latest point in 2-3 sentences."
                )
            }
        ]
        res2 = call_llm(provider=a2["provider"], model=a2.get("model"), messages=a2_messages)
        transcript.append({
            "speaker": a2["name"],
            "provider": a2["provider"],
            "model": res2["model"],
            "message": res2["content"]
        })

        # --- AGENT 1 TURN (if rounds remain) ---
        if round_idx < rounds:
            formatted_history = "\n".join([f"{t['speaker']}: {t['message']}" for t in transcript])
            a1_messages = [
                {"role": "system", "content": a1["personality"]},
                {
                    "role": "user",
                    "content": (
                        f"The debate topic is: '{topic}'.\n"
                        f"The dialogue so far:\n{formatted_history}\n\n"
                        f"Rebut {a2['name']}'s argument directly in 2-3 sentences."
                    )
                }
            ]
            res1_next = call_llm(provider=a1["provider"], model=a1.get("model"), messages=a1_messages)
            transcript.append({
                "speaker": a1["name"],
                "provider": a1["provider"],
                "model": res1_next["model"],
                "message": res1_next["content"]
            })

    return {
        "status": "success",
        "topic": topic,
        "total_turns": len(transcript),
        "agents": {
            "agent_1": {"name": a1["name"], "provider": a1["provider"], "model": a1.get("model")},
            "agent_2": {"name": a2["name"], "provider": a2["provider"], "model": a2.get("model")}
        },
        "transcript": transcript
    }

def run_three_way_round_robin(
    topic: str,
    rounds: int = 2,
    agent_1_cfg: Optional[Dict[str, Any]] = None,
    agent_2_cfg: Optional[Dict[str, Any]] = None,
    agent_3_cfg: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Executes a 3-agent round-robin conversation.
    Demonstrates the Week 2 Day 1 advanced exercise (Alex vs Blake vs Pierre).
    """
    agents = [
        agent_1_cfg or {
            "name": "Alex",
            "provider": "openai",
            "model": "gpt-4o-mini",
            "personality": "You are Alex, hyper-critical, witty, and always pointing out risks and costs."
        },
        agent_2_cfg or {
            "name": "Blake",
            "provider": "ollama",
            "model": "llama3.2",
            "personality": "You are Blake, practical, data-driven, and focused on business execution."
        },
        agent_3_cfg or {
            "name": "Pierre",
            "provider": "groq",
            "model": "qwen/qwen3.8-27b",
            "personality": "You are Pierre, a philosophical thinker who connects technical topics to human impact and the bigger picture."
        }
    ]

    transcript: List[Dict[str, str]] = []

    # Opening turn from Agent 0
    init_res = call_llm(
        provider=agents[0]["provider"],
        model=agents[0].get("model"),
        messages=[
            {"role": "system", "content": agents[0]["personality"]},
            {"role": "user", "content": f"Topic: '{topic}'. Share your opening perspective in 2 concise sentences."}
        ]
    )
    transcript.append({
        "speaker": agents[0]["name"],
        "provider": agents[0]["provider"],
        "model": init_res["model"],
        "message": init_res["content"]
    })

    # Round robin cycles
    for cycle in range(1, rounds + 1):
        for idx in range(len(agents)):
            # If cycle 1 and first agent already opened, skip to second
            if cycle == 1 and idx == 0:
                continue

            current_agent = agents[idx]
            other_names = ", ".join([a["name"] for i, a in enumerate(agents) if i != idx])
            
            history_text = "\n".join([f"{t['speaker']}: {t['message']}" for t in transcript])
            messages = [
                {"role": "system", "content": current_agent["personality"]},
                {
                    "role": "user",
                    "content": (
                        f"You are {current_agent['name']}, in a 3-way conversation with {other_names} on '{topic}'.\n"
                        f"Here is the dialogue so far:\n{history_text}\n\n"
                        f"Respond to the previous speakers with your perspective as {current_agent['name']} in 2 sentences."
                    )
                }
            ]
            
            res = call_llm(
                provider=current_agent["provider"],
                model=current_agent.get("model"),
                messages=messages
            )
            transcript.append({
                "speaker": current_agent["name"],
                "provider": current_agent["provider"],
                "model": res["model"],
                "message": res["content"]
            })

    return {
        "status": "success",
        "topic": topic,
        "cycles": rounds,
        "total_turns": len(transcript),
        "transcript": transcript
    }
