# ai/generators/youtube.py
from ai.text_generator import TextGenerator
from core.interfaces import ContentGenerator

class YouTubeGenerator(ContentGenerator):
    PROMPT = """\
TITLE
Exploring {set_name}: {artist}’s … (≤ 60 chars, no emoji)

DESCRIPTION
P1) We transform an ordinary town painting into the {set_name} LORA style (SDXL).  
P2) Technical: weight {weight}, CFG {cfg}, trigger “{trigger}”.  
P3) Emotional: {artist}’s palette & light.  
Hashtags: {seo_tags}
"""

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
            trigger=row.get("Trigger", row["SetName"].replace(" ", "")),
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
            title, desc = f"Exploring {row['SetName']} LoRA", raw

        return {"title": title, "description": desc}


# eski modül düzeyindeki fonksiyonu koruyalım (kırılım olmasın)
def generate(row: dict, cfg) -> dict:
    return YouTubeGenerator().generate(row, cfg)