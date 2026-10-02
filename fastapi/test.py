from app.services.huggingface import ask_huggingface

response = ask_huggingface(
    "Hello! Introduce yourself in one sentence."
)

print(response)