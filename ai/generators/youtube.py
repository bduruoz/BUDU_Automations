# BUDU AUTOMATIONS 2026
# ai/generators/youtube.py
from ast import pattern
import re
from ai.text_generator import TextGenerator
from core.interfaces import ContentGenerator
import configs.explora_cfg as cfg

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
        prompt = build_desc_prompt(
            pool_size = cfg.DESCRIPTION_POOL_SIZE,
            max_words = cfg.DESCRIPTION_MAX_WORDS,
            desc_marker = cfg.DESC_MARKER,
            set_name = row["Set Name"],
            is_artist = "Artist" in row, # bool: True ise sanatçı
            common_tags = " ".join(cfg.COMMON_TAGS),
            seo = " ".join(cfg.SEO_KEYWORDS),
        )
        raw = self._txtgen.generate(prompt, max_tokens=800)
        
        print("=== RAW DESCRIPTION === ", raw)
        
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
def build_desc_prompt(*, pool_size: int, max_words: int, desc_marker: str, set_name: str, is_artist: bool, common_tags: str, seo: str) -> str:
    body = cfg.DESCRIPTION_ARTIST if is_artist else cfg.DESCRIPTION_GENERIC
    seo = " ".join(cfg.SEO_KEYWORDS)
    return f"""
You are a creative copy-editor who speaks ONLY in English.
Write {pool_size} DISTINCT descriptions (≤{max_words} words each) for LoRA "{set_name}".
Artist LoRA: {"yes" if is_artist else "no"}
Tone: {"artsy" if is_artist else "technical"}

Body:
{body}

Outro (add verbatim):
{cfg.DESCRIPTION_OUTRO}

Output:
{desc_marker}1: <text>
{desc_marker}2: <text>
...
{desc_marker}{pool_size}: <text>
"""

def pick_best_desc(reply: str, scorer=None) -> str:
    pattern = rf"{re.escape(cfg.DESC_MARKER)}\d+:\s(.*)"
    chunks = [m.group(1) for m in re.finditer(pattern, reply, re.S)]

    if not chunks:
        return reply.strip()
    if scorer is None:
        return max(chunks, key=lambda c: len(c.split())).strip()

    scored = [(c.strip(), scorer.score(c)) for c in chunks if c.strip()]

    return max(scored, key=lambda x: x[1])[0]