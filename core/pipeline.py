# core/pipeline.py
import types, re
from pathlib import Path
from configs.explora_cfg import DESCRIPTION_TEMP
from data.file_scanner     import FileScanner
from data.metadata_builder import MetaDataBuilder
from data.excel_manager    import ExcelManager
from ai.generators.youtube import YouTubeGenerator, build_desc_prompt, pick_best_desc
from ai.text_generator     import TextGenerator

class ContentPipeline:
    def __init__(self, config):
        self.cfg = types.SimpleNamespace(**config)
        self.excel = ExcelManager(
            self.cfg.EXCEL_PATH,
            colors={
                "header":     self.cfg.HEADER_COLOR,
                "true":       self.cfg.TRUE_COLOR,
                "false":      self.cfg.FALSE_COLOR,
                "error":      self.cfg.ERROR_COLOR,
                "zebra_dark": self.cfg.ZEBRA_DARK,
            }
        )

    def run(self):
        print("▶ Content Pipeline Started")
        lora_sets = FileScanner(self.cfg.TOPUBLISH_DIR).scan()
        if not lora_sets:
            print("ℹ  No new LoRA set found.")
            return

        yt_gen = YouTubeGenerator()
        for row in lora_sets:
            # MetaDataBuilder only fills technical metadata
            meta = MetaDataBuilder(self.cfg.TOPUBLISH_DIR).scan()
#                                   row["lora_path"],
#                                   row["Set Name"],
#                                   row["Created At"]).build()
            #row.update(meta)

            name      = row["Set Name"]
            is_artist = "artist" in name.lower()

            # 1) Description pool
            prompt = build_desc_prompt(name, is_artist,
                                       " ".join(self.cfg.COMMON_TAGS),
                                       " ".join(self.cfg.SEO_KEYWORDS))
            raw = TextGenerator(base_url=self.cfg.LM_STUDIO_URL,
                                model=self.cfg.LM_MODEL_NAME,
                                temperature=DESCRIPTION_TEMP).generate(prompt,
                                                                       max_tokens=900)
            best_desc = pick_best_desc(raw)

            # 2) Title Create
            yt = yt_gen.generate(row, self.cfg)
            row["Youtube Title"]       = yt["title"]
            row["Youtube Description"] = best_desc

        added = self.excel.add_new_sets(lora_sets)
        print(f"✔  {added} new sets added to Excel")

    def _scan(self):
        return FileScanner(self.cfg.TOPUBLISH_DIR).scan()
    