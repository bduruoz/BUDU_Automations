# ai/text_generator.py
import time, requests
from pathlib import Path
from configs.explora import RATE_LIMIT_CALLS, RATE_LIMIT_PERIOD

class TextGenerator:
    def __init__(self, base_url: str, model: str, temperature: float = 0.75):
        self.url  = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.temp = temperature
        self._calls = []          # simple sliding-window

    def _wait_if_needed(self):
        now = time.time()
        self._calls = [t for t in self._calls if now - t < RATE_LIMIT_PERIOD]
        if len(self._calls) >= RATE_LIMIT_CALLS:
            sleep_t = self._calls[0] + RATE_LIMIT_PERIOD - now
            if sleep_t > 0:
                time.sleep(sleep_t)
        self._calls.append(time.time())

    def generate(self, prompt: str, max_tokens: int = 300) -> str:
        self._wait_if_needed()
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temp,
            "max_tokens": max_tokens
        }
        resp = requests.post(self.url, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    