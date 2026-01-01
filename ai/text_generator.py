# ai/text_generator.py
import openai, os
from pathlib import Path

class TextGenerator:
    def __init__(self, base_url: str, model: str, temperature: float = 0.75):
        self.client = openai.OpenAI(
            api_key="lm-studio",          # gereksiz ama boş bırakılmıyor
            base_url=base_url
        )
        self.model = model
        self.temp = temperature

    def generate(self, prompt: str, max_tokens: int = 300) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temp,
            max_tokens=max_tokens
        )
        return resp.choices[0].message.content.strip()