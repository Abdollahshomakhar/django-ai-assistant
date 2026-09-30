import json
import re

import httpx  # already installed as a dependency of openai

# OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_URL = "http://host.docker.internal:11434/api/chat"

MODEL = "qwen2.5-coder:3b"
NUM_CTX = 8192
TIMEOUT = 180


class LLMError(Exception):
    pass


def chat(messages, temperature=0.3, json_mode=False):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_ctx": NUM_CTX,
        },
    }

    if json_mode:
        payload["format"] = "json"

    try:
        response = httpx.post(
            OLLAMA_URL,
            json=payload,
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        content = response.json()["message"]["content"] or ""

    except (httpx.HTTPError, KeyError, ValueError) as exc:
        raise LLMError(
            f"Ollama request failed: {exc}"
        ) from exc

    return re.sub(
        r"<think>.*?</think>",
        "",
        content,
        flags=re.S,
    ).strip()


def chat_json(messages, retries=1):
    last = None
    for _ in range(retries + 1):
        raw = chat(messages, temperature=0, json_mode=True)
        text = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.M).strip()
        start, end = text.find("{"), text.rfind("}")
        try:
            data = json.loads(text[start:end + 1])
            if isinstance(data, dict):
                return data
        except ValueError as exc:
            last = exc
    raise LLMError("LLM returned invalid JSON") from last
