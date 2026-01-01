# ai/generators/youtube.py
# -*- coding: utf-8 -*-
"""
YouTube title + description generator
Yeni özellikler:
- Teknik detay (weight, CFG, trigger)
- Stil özeti (fırça, ışık, kompozisyon)
- Duygusal ama hâlâ SEO'lu
- Emoji yok, < 60 char title, < 2 200 char description
"""

from ai.base_prompt import * #llm_generate   # senin txtgen wrapper’ın

# ------------------------------------------------------
# 1) PROMPT ŞABLONU – tek prompt’ta title + description
# ------------------------------------------------------
PROMPT = """\
Finish the text below in EXACT order. Do NOT add headings or labels.

TITLE (start with "Exploring {set_name}: {artist}’s …", ≤ 60 chars, no hashtags, no quotes)

DESCRIPTION
Paragraph 1 (40-60 words): Hook + explain we take an ordinary town photo and re-render it in the {set_name} LORA style (SDXL).  
Paragraph 2 (70-90 words): Technical – recommended weight {weight}, CFG {cfg}, trigger “{trigger}”, positive prompt example, why it enhances base SDXL.  
Paragraph 3 (40-50 words): Emotional – artist’s brush, colour palette, light philosophy.  
Last line: 5-6 hashtags + {seo_tags}

SET:      {set_name}
ARTIST:   {artist}
TRIGGER:  {trigger}
WEIGHT:   {weight}
CFG:      {cfg}
SEO_TAGS: {seo_tags}
"""

# ------------------------------------------------------
# 2) GENERATE FONKSİYONU
# ------------------------------------------------------
def generate(row: dict, cfg) -> dict:
    """
    row: file_scanner dict
    cfg: configs.explora modülü
    """
    # metadata_builder’dan gelen teknik alanlar
    prompt = PROMPT.format(
        set_name   = row["SetName"],
        artist     = row["Artist"],
        trigger    = row.get("Trigger", row["SetName"].replace(" ", "")),
        weight     = row.get("Weight", "0.75-0.9"),
        cfg        = row.get("CFG", "6-8"),
        seo_tags   = " ".join(cfg.COMMON_TAGS + cfg.SEO_KEYWORDS)
    )

    raw = llm_generate(prompt, max_tokens=800, temperature=0.65)

    # LM-Studio çıktısını ayır
    try:
        title_part, desc_part = raw.split("DESCRIPTION", 1)
        title = title_part.replace("TITLE", "").strip()
        desc  = desc_part.strip()
    except ValueError:          # LM bazen format bozuyor
        title = f"Exploring {row['SetName']} LoRA"
        desc  = raw

    return {"title": title, "description": desc}

# Eski adla uyumlu
def run(row: dict, cfg) -> dict:
    return generate(row, cfg)