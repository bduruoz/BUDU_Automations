# core/pipeline.py
import types
from pathlib import Path
from data.metadata_builder import FileScanner 
from ai.generators.youtube import YouTubeGenerator
from AI_Automations.data.file_scanner import scan
from AI_Automations.data.excel_manager import ExcelManager

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
    