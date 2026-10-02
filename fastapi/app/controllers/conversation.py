from app.services.llm_conversation import start_conversation


def create_conversation(topic):

    return start_conversation(
        topic,
        rounds=5
    )

from app.services.interview import start_interview


def run_interview():

    return start_interview()