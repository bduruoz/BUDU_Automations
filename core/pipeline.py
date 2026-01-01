# core/pipeline.py
# en üst
from ai.generators.youtube import YouTubeGenerator
from pathlib import Path
import types  # <-- ekle
from AI_Automations.data.file_scanner import scan
from AI_Automations.data.excel_manager import ExcelManager

class ContentPipeline:
    def __init__(self, config):
        self.cfg = types.SimpleNamespace(**config)  # dict → object
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
        print("▶ ContentPipeline başladı")
        lora_sets = scan(self.cfg.BASE_DIR)
        if not lora_sets:
            print("ℹ Yeni set bulunamadı")
            return
        
        yt_gen = YouTubeGenerator()
        for row in lora_sets:
            yt = yt_gen.generate(row, self.cfg)
            row["Youtube Title"]       = yt["title"]
            row["Youtube Description"] = yt["description"]
        
        added = self.excel.add_new_sets(lora_sets)
        print(f"✔ Excel’e eklenen yeni set: {added}")
        
    def _scan(self):
        return scan(self.cfg.BASE_DIR)
    
    
    
    
    
    
    
    
    
    
    
    
