# ai/text_generator.py
import time, requests
from pathlib import Path
from configs.explora import RATE_LIMIT_CALLS, RATE_LIMIT_PERIOD
from utils.rate_limiter import RateLimiter

RATE = RateLimiter(max_calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_PERIOD)

class TextGenerator:
    def __init__(self, base_url: str, model: str, temperature: float = 0.75):
        self.url   = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.temp  = temperature

    @RATE
    def generate(self, prompt: str, max_tokens: int = 300) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temp,
            "max_tokens": max_tokens
        }
        resp = requests.post(self.url, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    
    