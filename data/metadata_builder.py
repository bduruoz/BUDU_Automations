# data/metadata_builder.py
from pathlib import Path
from datetime import datetime

VIDEO_EXTENSIONS = {".mp4", ".mov"}

# ---------- 1) SANATÇI EŞLEME (isteğe bağlı genişlet) ----------
# Set ismine göre "Artist" ve teknik değerler
ARTIST_MAP = {
    "Andreas Achenbach": {
        "Artist": "Andreas Achenbach",
        "Trigger": "aachenbach",
        "Weight": "0.8-0.9",
        "CFG": "7-8",
    },
    "Ivan Shishkin": {
        "Artist": "Ivan Shishkin",
        "Trigger": "shishkin",
        "Weight": "0.75-0.85",
        "CFG": "6-7",
    },
    # yeni set eklendiğinde buraya bir satır daha
}

class FileScanner:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def scan(self) -> list[dict]:
        results: list[dict] = []
        sets: dict[str, dict] = {}

        for path in self.root.iterdir():
            if not path.is_file() or path.suffix.lower() not in VIDEO_EXTENSIONS:
                continue

            parts = path.stem.split("_")
            if len(parts) != 2:
                continue

            set_name_raw, category = parts
            set_name = ''.join([' ' + c if c.isupper() else c for c in set_name_raw]).strip()

            # ---------- 2) TEKNİK ALANLARI EKLE ----------
            tech = ARTIST_MAP.get(set_name, {
                "Artist": set_name,               # fallback
                "Trigger": set_name.replace(" ", ""),
                "Weight": "0.75-0.9",
                "CFG": "6-8",
            })

            if set_name not in sets:
                sets[set_name] = {
                    "SetName": set_name,          # youtube.py'nin beklediği key
                    "Artist": tech["Artist"],
                    "Trigger": tech["Trigger"],
                    "Weight": tech["Weight"],
                    "CFG": tech["CFG"],
                    "Created At": self._get_created_date(path),
                    "MP4": False,
                    "MOV": False,
                    "Square": False,
                    "Preview": False,
                    "Youtube": False,
                    "Vimeo": False,
                    "Duruoz": False,
                    "Linkedin": False,
                    "Tumblr": False,
                    "Mastodon": False,
                    "BlueSky": False,
                    "Twitter": False,
                    "Instagram": False,
                    "Youtube Shorts": False,
                    "Facebook": False,
                }

            # kategori → sütun map (eski)
            col = {"ProRes": "MOV", "Youtube": "MP4", "Square": "Square", "Preview": "Preview"}.get(category)
            if col:
                sets[set_name][col] = path

        return list(sets.values())

    # ---------- 3) TARİH YARDIMCI ----------
    def _get_created_date(self, path: Path) -> datetime:
        return datetime.fromtimestamp(path.stat().st_ctime)
    