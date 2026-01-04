# BUDU AUTIMATIONS 2026
# data/file_scanner.py

from pathlib import Path
from datetime import datetime

VIDEO_EXT = {".mp4", ".mov"}
IMAGE_EXT = {".png"}

class FileScanner:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        
    def scan(self) -> dict:
        sets = {} # set_name -> dict

        print("Scanning directory:", self.root)

        for p in self.root.iterdir():
            if not p.is_file():
                continue
            ext = p.suffix.lower()
            if ext not in VIDEO_EXT | IMAGE_EXT:
                continue

            stem = p.stem
            if "_" not in stem:
                continue
            
            set_name_raw, suffix = stem.rsplit("_", 1)          # AndreasAchenbach , Preview

            # CamelCase → space
            set_name = ""
            for i, ch in enumerate(set_name_raw):
                if i and ch.isupper():
                    set_name += " "
                set_name += ch
            
            # Create Set if not exists
            if set_name not in sets:
                sets[set_name] = {
                    "Set Name": set_name,
                    "MP4": False,
                    "MOV": False,
                    "Square": False,
                    "Preview": False,
                    "Created At": datetime.fromtimestamp(p.stat().st_mtime),
                    "Discovered At": datetime.now().replace(microsecond=0),
                    "Published At": None,
                    "Youtube": False,
                    "Vimeo": False,
                    "DuruozNet": False,
                    "Linkedin": False,
                    "Tumblr": False,
                    "Mastodon": False,
                    "BlueSky": False,
                    "Twitter": False,
                    "Instagram": False,
                    "Shorts": False,
                    "Facebook": False,
                    "Path": str(p),
                }

            # flag’leri aç
            if suffix == "Youtube" and ext == ".mp4":
                sets[set_name]["MP4"] = True
            elif suffix == "ProRes" and ext == ".mov":
                sets[set_name]["MOV"] = True
            elif suffix == "Square" and ext == ".mp4":
                sets[set_name]["Square"] = True
            elif suffix == "Preview" and ext == ".png":
                sets[set_name]["Preview"] = True

        return list(sets.values())