# configs/explora.py
from pathlib import Path

BASE_DIR = Path(r"E:\AI-Outputs\LoraWeights\Publish")
PUBLISHED_DIR = BASE_DIR / "Published"
EXCEL_PATH = BASE_DIR / "expLora_registry.xlsx"

# Color Palette
HEADER_COLOR = "#D9E1F2"
TRUE_COLOR   = "#7DEF94"
FALSE_COLOR  = "#F06979"
ERROR_COLOR  = "#FFBDC7"
ZEBRA_DARK   = "#E8E8E8"

LM_STUDIO_URL   = "http://localhost:9090/v1"
LM_MODEL_NAME   = "openai/gpt-oss-120b"
#TEMPERATURE     = 0.75          # eski generator için

# Rate-Limit
RATE_LIMIT_CALLS  = 30
RATE_LIMIT_PERIOD = 60          # saniye

# SEO & Tags
SEO_KEYWORDS  = ["AI art", "ComfyUI", "LoRA", "Stable Diffusion",
                 "AI generated art", "AI illustrations", "AI creativity",
                 "AI image generation", "SDXL", "Dream Shaper"]
COMMON_TAGS   = ["#AIart", "#ComfyUI", "#LoRA", "#StableDiffusion",
                 "#AIGeneratedArt", "#AIillustration", "#AIcreativity",
                 "#AIimageGeneration", "#SDXL", "#DreamShaper"]
INCLUDE_LINKS = True
LINKS = ["https://duruoz.net/watch/{set_name}",
         "https://duruoz.net/blog/{set_name}"]

SERIES_TAG = "Exploring LORA"

# Prompt Delimiters
TITLE_MARKER = "### Title:"
DESC_MARKER  = "### Description:"

# Pool Settings
DESCRIPTION_POOL_SIZE   = 5
TITLE_POOL_SIZE         = 5
DESCRIPTION_MAX_WORDS   = 90
DESCRIPTION_TEMP        = 0.9
DESCRIPTION_REFINE_TEMP = 0.4

# Text Blocks
DESCRIPTION_ARTIST = """
{set_name} LoRA's AI-reimagined weird world.
In this visual experiment we test how weight slides (0.01 → 3.0) affect the render.
Watch every frame evolve in complexity, line-detail and stylistic appeal.
"""

DESCRIPTION_GENERIC = """
Step into the eerie aesthetics of {set_name} LoRA.
This visual test inspects how 0.01-3.0 weight steps change style, mood & intensity.
Each frame shows gradual shifts and how tiny deltas can transform the final output.
"""

DESCRIPTION_OUTRO = """
Command & model kept constant.
Only LoRA weight changes per frame.
Created entirely in ComfyUI.
Base model: Dreamshaper XL Lightning
LoRA: {set_name}
{common_tags}  {seo_keywords}
"""