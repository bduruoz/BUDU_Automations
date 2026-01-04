# BUDU AUTIMATIONS 2026
# data/metadata_builder.py

from pathlib import Path
from datetime import datetime

VIDEO_EXTENSIONS = {".mp4", ".mov"}
IMAGE_EXTENSIONS = {".png"}

# sonra düzenlenecek. (muhtemelen dosyadan okunacak)
# Trigger Wright ve CFG değerleri gerekmeyebilir
# is_artist burada belirlenebilir
LORA_MAP = {
    "Andreas Achenbach": {"Artist": "Andreas Achenbach", "Trigger": "aachenbach", "Weight": "0.8-0.9", "CFG": "7-8"},
    "Ivan Shishkin":     {"Artist": "Ivan Shishkin",     "Trigger": "shishkin",   "Weight": "0.75-0.85", "CFG": "6-7"},
}

class MetaDataBuilder:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def scan(self) -> list[dict]:
        sets: dict[str, dict] = {}

        print("Meta Scanning directory:", self.root)

        for path in self.root.iterdir():

            if not path.is_file() or path.suffix.lower() not in VIDEO_EXTENSIONS | IMAGE_EXTENSIONS:
                continue

            parts = path.stem.split("_")
            if len(parts) != 2:
                continue
            set_name_raw, category = parts
            set_name = ''.join([' ' + c if c.isupper() else c for c in set_name_raw]).strip()

            # 1) tech metadata from LORA_MAP
            tech = LORA_MAP.get(set_name) or {
                "Artist": set_name,
                "Trigger": set_name.replace(" ", ""),
                "Weight": "0.75-0.9",
                "CFG": "6-8",
            }

            # 2) Create Set if not exists
            if set_name not in sets:
                sets[set_name] = {
                    "Set Name": set_name,
                    **tech,                         # add all at once
                    "Created At": self._get_created_date(path),
                    "MP4": False, "MOV": False, "Square": False, "Preview": False,
                    "Youtube": False, "Vimeo": False, "Duruoz": False,
                    "Linkedin": False, "Tumblr": False, "Mastodon": False,
                    "BlueSky": False, "Twitter": False, "Instagram": False,
                    "Youtube Shorts": False, "Facebook": False,
                }

            # 3) Fill in the category column
            if category == "Preview":
                sets[set_name]["Preview"] = True
                sets[set_name]["Path"] = str(path)
            else:
                col = {"ProRes": "MOV", "Youtube": "MP4", "Square": "Square"}.get(category)
                if col:
                    sets[set_name][col] = path

        return list(sets.values())

    def _get_created_date(self, path: Path) -> datetime:
        return datetime.fromtimestamp(path.stat().st_mtime)
    