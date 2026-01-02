# core/pipeline.py
import types
from pathlib import Path
from cv2 import line
from data.metadata_builder import FileScanner 
from ai.generators.youtube import YouTubeGenerator
from AI_Automations.data.file_scanner import scan
from AI_Automations.data.excel_manager import ExcelManager
from configs.explora import TITLE_MARKER, DESC_MARKER
from ai.text_generator import LMStudioGenerator

class ContentPipeline:
    def __init__(self, config):
        self.cfg = types.SimpleNamespace(**config)
        self.excel = ExcelManager(
            self.cfg.EXCEL_PATH,
            colors={
                "header": self.cfg.HEADER_COLOR,
                "true":   self.cfg.TRUE_COLOR,
                "false":  self.cfg.FALSE_COLOR,
                "error":  self.cfg.ERROR_COLOR,
                "zebra_dark": self.cfg.ZEBRA_DARK,
            }
        )

    def run(self):
        print("▶ Content Pipeline Started")
        lora_sets = FileScanner(self.cfg.BASE_DIR).scan() 
        if not lora_sets:
            print("ℹ New LORA Set Not Found !")
            return
        
        # Prompt Title and Description Extraction
        if line.startswith(TITLE_MARKER):
            title = line.replace(TITLE_MARKER, "").strip()
        if line.startswith(DESC_MARKER):
            description = line.replace(DESC_MARKER, "").strip()
        
        # Youtube Metinleri Oluştur
        yt_gen = YouTubeGenerator()
        for row in lora_sets:
            yt = yt_gen.generate(row, self.cfg)
            row["Youtube Title"]       = yt["title"]
            row["Youtube Description"] = yt["description"]
        
        added = self.excel.add_new_sets(lora_sets)
        print(f"✔ {added} new sets added to Excel")
        
    def _scan(self):
        return FileScanner(self.cfg.BASE_DIR).scan()
    
    def build_description_pool(self, set_name: str, is_artist: bool, common_tags: str, seo: str) -> list[str]:
        prompt = (
            DESCRIPTION_WRITER
            .replace("{{set_name}}", set_name)
            .replace("{{is_artist}}", "yes" if is_artist else "no")
            .replace("{{common_tags}}", common_tags)
            .replace("{{seo_keywords}}", seo))
        lmstudio = LMStudioGenerator()
        reply = lmstudio.chat(prompt, temp=0.9)   # yüksek çeşitlilik
        chunks = re.split(r"### Desc-\d+:\s*", reply)[1:]  # ilk eleman boş
        return [c.strip() for c in chunks if c.strip()]