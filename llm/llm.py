import requests

def llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"qwen2.5:3b",
            "prompt":prompt,
            "stream":False
        }
    )

    return response.json()["response"]