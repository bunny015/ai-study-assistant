import time
from openai import OpenAI
from config.settings import OPENROUTER_API_KEY, OPENROUTER_MODEL


class LLMClient:
    def __init__(self, api_key=OPENROUTER_API_KEY, model=OPENROUTER_MODEL):
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            timeout=60.0,
        )

    def chat(self, messages, temperature=0.7, max_attempts=3):
        last_error = None
        for attempt in range(max_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                )
                return response.choices[0].message.content or ""
            except Exception as exc:
                last_error = exc
                status = getattr(exc, "status_code", None)
                retryable = status in {408, 429, 500, 502, 503, 504} or isinstance(exc, (TimeoutError, ConnectionError))
                if not retryable or attempt == max_attempts - 1:
                    raise
                time.sleep(2 ** attempt)
        raise last_error
