# configs/explora.py
from pathlib import Path

BASE_DIR = Path(r"E:\AI-Outputs\LoraWeights\Publish")
PUBLISHED_DIR = BASE_DIR / "Published"
EXCEL_PATH = BASE_DIR / "expLora_registry.xlsx"

# istediğin renk paleti
HEADER_COLOR = "#D9E1F2"
TRUE_COLOR   = "#7DEF94"
FALSE_COLOR  = "#F06979"
ERROR_COLOR  = "#FFBDC7"
ZEBRA_DARK   = "#E8E8E8"

LM_STUDIO_URL = "http://localhost:9090/v1"
LM_MODEL_NAME = "openai/gpt-oss-120b"   # kurulu model
SEO_KEYWORDS  = ["AI art", "stable diffusion", "lora"]
COMMON_TAGS   = ["#AIart", "#StableDiffusion", "#Lora"]
INCLUDE_LINKS = True
LINKS = ["https://duruoz.net/watch/{set_name}",
         "https://duruoz.net/blog/{set_name}"]

SERIES_TAG = "Exploring LORA"   # şimdilik kullanmasak da kalsın
TEMPERATURE   = 0.75


