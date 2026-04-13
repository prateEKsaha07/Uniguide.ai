import json
import requests

def ask_llm(context, query):
    if not context.strip():
        return "Not in syllabus"

    prompt = f"""
You are a strict academic assistant.
Follow these rules strictly:

1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. If answer is not in context, reply exactly:
   "Not in syllabus"

4. Understand the question type:

- If user asks to explain → give full explanation.
- If user asks to list topics → list them.
- If user asks for count → count them.

5. DEFAULT BEHAVIOR:
If the user does NOT explicitly ask for explanation,
then:
- give SHORT definitions (1 line each)
- keep answers concise

6. Always keep answers structured.

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
    

    