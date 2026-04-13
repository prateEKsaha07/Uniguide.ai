import json
import requests

def ask_llm(context, query):
    if not context.strip():
        return "Not in syllabus"

    prompt = f"""
You are a strict academic assistant.

You MUST follow these rules:

1. Answer ONLY using the provided context.
2. Do NOT use any outside knowledge.
3. If the answer is not clearly in the context, reply exactly:
   "Not in syllabus"

4. If the answer IS present:
   - Start with a clear definition
   - Then give bullet points
   - Keep it simple and accurate

Context:
{context}

Question:
{query}

Answer:
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 200
                }
            },
            timeout=60,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        return f"error contacting LLM: {exc}"

    try:
        data = response.json()
        return data.get("response", "error: missing response field").strip()
    except ValueError:
        full_text = ""
        for line in response.text.splitlines():
            try:
                payload = json.loads(line)
                if "response" in payload:
                    full_text += payload["response"]
            except ValueError:
                continue

        return full_text.strip() if full_text else "error in getting response from LLM"