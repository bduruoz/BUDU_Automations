# ai/generators/youtube.py
from ai.text_generator import TextGenerator
from core.interfaces import ContentGenerator
from explora import TITLE_MARKER, DESC_MARKER

class YouTubeGenerator(ContentGenerator):
    DESCRIPTION_WRITER = f"""
You are a creative copy-editor who speaks ONLY in English.

TASK:
- LoRA name: {{set_name}}
- Artist LoRA ? {{is_artist}}   (yes/no)
- Common tags: {{common_tags}}
- SEO keywords: {{seo_keywords}}

Write 5 DISTINCT English descriptions (max 90 words each).
Each must:
1. Start with an intriguing one-liner.
2. Middle: explain the weight-test (0.01 → 3.0) and visual changes.
3. End with the fixed outro block below.
4. Keep tone {{"artsy" if is_artist else "technical"}}.
5. NO Turkish, NO emoji, NO “Lora” capitalised wrong.

Output format:
### Desc-1:
<text>

### Desc-2:
<text>
...
### Desc-5:
<text>

Fixed outro (add verbatim):
ComfyUI only. Dreamshaper XL Lightning base.
LoRA: {{set_name}}
{{common_tags}}
{{seo_keywords}}
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

# eski modül düzeyindeki fonksiyonu koruyalım (kırılım olmasın)
def generate(row: dict, cfg) -> dict:
    return YouTubeGenerator().generate(row, cfg)

    
#    PROMPT = f"""{TITLE_MARKER}
#Exploring LoRA: {{set_name}} - {{simple_desc}}
###
#DESCRIPTION
#P1) We transform an ordinary town painting into the {set_name} LORA style (SDXL).  
#P2) Technical: weight {weight}, CFG {cfg}, trigger “{trigger}”.  
#P3) Emotional: {artist}’s palette & light.  
#Hashtags: {seo_tags}
