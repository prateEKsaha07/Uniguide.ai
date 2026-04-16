import json
import requests


def detect_intent(query):
    q = query.lower()

    if "how many" in q or "count" in q:
        return "count"
    if "list" in q or "topics" in q:
        return "list"
    if "learning path" in q or "roadmap" in q:
        return "path"

    return "default"


def ask_llm(context, query):
    if not context.strip():
        return "Not in syllabus"

    intent = detect_intent(query)

    prompt = f"""
You are a STRICT syllabus assistant.

You MUST follow rules EXACTLY.

RULES:
1. Use ONLY the given context
2. If answer not present → reply EXACTLY: Not in syllabus

3. OUTPUT FORMAT RULES (MANDATORY):

IF intent = count:
- Output ONLY a number
- No explanation

IF intent = list:
- Output ONLY topic names
- One per line
- No explanation

IF intent = path:
- Output ordered steps
- Use numbering (1,2,3...)

IF intent = default:
- Give SHORT definition (1–2 lines max)

DO NOT:
- Add extra explanation
- Add examples
- Add introduction or conclusion

Context:
{context}

Question:
{query}

Intent:
{intent}

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
                    "temperature": 0.1,
                    "num_predict": 150
                }
            },
            timeout=60,
        )
        response.raise_for_status()

    except requests.RequestException as exc:
        return f"error contacting LLM: {exc}"

    try:
        data = response.json()
        result = data.get("response", "").strip()

    except ValueError:
        result = ""
        for line in response.text.splitlines():
            try:
                payload = json.loads(line)
                if "response" in payload:
                    result += payload["response"]
            except ValueError:
                continue
        result = result.strip()

    if not result:
        return "error in getting response from LLM"

    return result