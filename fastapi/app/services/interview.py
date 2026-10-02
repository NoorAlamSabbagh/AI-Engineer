from app.services.openai_service import ask_openai as ask_suresh
from app.services.huggingface import ask_huggingface as ask_ramesh


def start_interview():

    conversation = [
        {
            "speaker": "System",
            "message": """
You are Suresh, a senior GenAI developer interviewer.

You are interviewing Ramesh for a GenAI Developer position.

Conduct a technical interview with exactly 10 questions.

Cover topics such as:

- Python
- LLMs
- Prompt Engineering
- Embeddings
- RAG
- Vector Databases
- LangChain / AI frameworks
- Agents
- LLM evaluation
- Production GenAI systems

Ask only ONE question at a time.

After Ramesh answers, ask the next question.

Do not provide feedback during the interview.

After question 10 has been answered, provide detailed
interview feedback.
"""
        }
    ]

    # -------------------------
    # 10 interview questions
    # -------------------------

    for question_number in range(1, 11):

        # Suresh asks question
        suresh_prompt = conversation + [
            {
                "speaker": "Instruction",
                "message": f"""
Ask interview question {question_number}.

You are Suresh.

Ask only the question.
Do not answer it yourself.
"""
            }
        ]

        question = ask_suresh(
            format_for_openai(suresh_prompt)
        )

        print(f"\nSuresh - Question {question_number}:")
        print(question)

        conversation.append({
            "speaker": "Suresh",
            "message": question
        })

        # -------------------------
        # Ramesh answers
        # -------------------------

        ramesh_prompt = conversation + [
            {
                "speaker": "Instruction",
                "message": """
You are Ramesh, the candidate.

Answer Suresh's interview question.

Answer as a GenAI Developer candidate.

Give a technically detailed but natural interview answer.
"""
            }
        ]

        answer = ask_ramesh(
            format_for_huggingface(ramesh_prompt)
        )

        print("\nRamesh:")
        print(answer)

        conversation.append({
            "speaker": "Ramesh",
            "message": answer
        })

    # -------------------------
    # Final feedback
    # -------------------------

    feedback_prompt = conversation + [
        {
            "speaker": "Instruction",
            "message": """
You are Suresh, the interviewer.

The interview is now complete.

Review all 10 questions and Ramesh's answers.

Provide detailed interview feedback.

Include:

1. Overall performance summary
2. Technical strengths
3. Technical weaknesses
4. Questions answered well
5. Questions that need improvement
6. Missing GenAI concepts
7. Communication quality
8. Suggested topics to study
9. Final interview assessment

Do not ask another question.
"""
        }
    ]

    feedback = ask_suresh(
        format_for_openai(feedback_prompt)
    )

    print("\n========== suresh_prompt ==========")
    # print(feedback)
    print(suresh_prompt)
    print("\n========== ramesh ==========")
    print(ramesh_prompt)

    conversation.append({
        "speaker": "Suresh",
        "message": feedback
    })

    return conversation

def format_for_openai(conversation):

    messages = []

    for item in conversation:

        messages.append({
            "role": "user",
            "content": f"{item['speaker']}: {item['message']}"
        })

    return messages


def format_for_huggingface(conversation):

    messages = []

    for item in conversation:

        messages.append({
            "role": "user",
            "content": f"{item['speaker']}: {item['message']}"
        })

    return messages