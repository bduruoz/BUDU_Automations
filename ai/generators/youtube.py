# ai/generators/youtube.py
import re
from ai.text_generator import TextGenerator
from core.interfaces import ContentGenerator
from configs.explora import (DESCRIPTION_POOL_SIZE, DESCRIPTION_MAX_WORDS,
                             DESCRIPTION_ARTIST, DESCRIPTION_GENERIC,
                             DESCRIPTION_OUTRO, DESC_MARKER)

class YouTubeGenerator(ContentGenerator):
    def __init__(self) -> None:
        self._txtgen: TextGenerator | None = None

    def generate(self, row: dict, cfg) -> dict:
        if self._txtgen is None:
            self._txtgen = TextGenerator(
                base_url=cfg.LM_STUDIO_URL,
                model=cfg.LM_MODEL_NAME,
                temperature=cfg.TEMPERATURE,
            )
        prompt = self.PROMPT.format(
            set_name=row["Set Name"],
            artist=row["Artist"],
            trigger=row.get("Trigger", row["Set Name"].replace(" ", "")),
            weight=row.get("Weight", "0.75-0.9"),
            cfg=row.get("CFG", "6-8"),
            seo_tags=" ".join(cfg.COMMON_TAGS + cfg.SEO_KEYWORDS),
        )
        raw = self._txtgen.generate(prompt, max_tokens=800)
        try:
            title, desc = raw.split("DESCRIPTION", 1)
            title = title.replace("TITLE", "").strip()
            desc = desc.strip()
        except ValueError:
            title, desc = f"Exploring {row['Set Name']} LoRA", raw
        return {"title": title, "description": desc}

# module-level fallback
def generate(row: dict, cfg) -> dict:
    return YouTubeGenerator().generate(row, cfg)

# pool helpers
def build_desc_prompt(set_name: str, is_artist: bool,
                      common_tags: str, seo: str) -> str:
    body = DESCRIPTION_ARTIST if is_artist else DESCRIPTION_GENERIC
    return f"""
You are a creative copy-editor who speaks ONLY in English.
Write {DESCRIPTION_POOL_SIZE} DISTINCT descriptions (≤{DESCRIPTION_MAX_WORDS} words each) for LoRA "{set_name}".
Artist LoRA: {"yes" if is_artist else "no"}
Tone: {"artsy" if is_artist else "technical"}

Body:
{body}

Outro (add verbatim):
{DESCRIPTION_OUTRO}

Output:
{DESC_MARKER}1: <text>
{DESC_MARKER}2: <text>
...
{DESC_MARKER}{DESCRIPTION_POOL_SIZE}: <text>
"""

def pick_best_desc(reply: str, scorer=None) -> str:
    chunks = re.findall(rf"(?<={re.escape(DESC_MARKER)}\d+:\s).*", reply, flags=re.S)
    if not chunks:
        return reply.strip()
    if scorer is None:
        return max(chunks, key=lambda c: len(c.split())).strip()
    scored = [(c.strip(), scorer.score(c)) for c in chunks if c.strip()]
    return max(scored, key=lambda x: x[1])[0]