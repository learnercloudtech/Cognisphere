import requests

def query_local_llm(prompt, model="llama3:2"):
    """
    Sends a prompt to the local LLM via Ollama and returns the response.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt}
        )
        return response.json()["response"]
    except Exception as e:
        return f"LLM query failed: {str(e)}"
