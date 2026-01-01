# data/excel_manager.py
import pandas as pd
from pathlib import Path

COLS = [
    "Set Name", "MP4", "MOV", "Square", "Preview",
    "Created At", "Discovered At", "Published At",
    "Youtube", "Vimeo", "DuruozNet", "Linkedin", "Tumblr",
    "Mastodon", "BlueSky", "Twitter", "Instagram", "Shorts", "Facebook",
    "Path"          # <-- yeni
]

class ExcelManager:
    def __init__(self, excel_path: str | Path, colors: dict | None = None):
        self.excel_path = Path(excel_path)
        self.colors = colors or {}          # varsayılan boş
        self.df = self._load_or_create()
        
        # ---------- load / create ----------
    def _load_or_create(self) -> pd.DataFrame:
        if self.excel_path.exists():
            df = pd.read_excel(self.excel_path)
            for c in COLS:
                if c not in df.columns:
                    df[c] = False if c not in {"Set Name","Created At","Discovered At","Published At","Path"} else None
            return df[COLS]
        return pd.DataFrame(columns=COLS)
    
    def add_new_sets(self, new_rows: list[dict]) -> int:
        existing = set(self.df["Set Name"].dropna().astype(str))
        added = 0
        for row in new_rows:
            if row["Set Name"] in existing:
                continue
            
            row["MP4"]     = bool(row.get("MP4", False))
            row["MOV"]     = bool(row.get("MOV", False))
            row["Square"]  = bool(row.get("Square", False))
            #row["Preview"] = bool(row.get("Preview"))
            
            
            
            
            row["Discovered At"] = pd.Timestamp.now()  # şu an
            row["Published At"]  = (pd.Timestamp(row["Published At"]) if pd.notna(row.get("Published At")) else "Non Published")
            platforms = ["Youtube", "Vimeo", "DuruozNet", "Linkedin", "Tumblr", "Mastodon", "BlueSky", "Twitter", "Instagram", "Shorts", "Facebook"]
            for col in platforms:
                val = row.get(col)
                if pd.isna(val):
                    row[col] = False          # başlangıçta hiçbiri yapılmamış
                else:
                    row[col] = bool(val)      # varsa True/False

            #path_obj = row.get("Preview")
            #row["Path"] = str(path_obj) if path_obj else "N/A"
            row["Path"] = str(row.get("Preview")) if row["Preview"] else "N/A"

            clean_row = {k: v for k, v in row.items() if k in COLS}
            # FutureWarning’siz ekleme
            self.df.loc[len(self.df)] = clean_row
            added += 1
        if added:
            self._save()
            print(f"✔ Excel güncellendi (bool sütunları düzeltildi): {self.excel_path}")
        return added

    def mark_published(self, set_name: str, platforms: list[str]):
        idx = self.df.index[self.df["Set Name"] == set_name]
        if idx.empty:
            return
        i = idx[0]
        for platform in platforms:
            if platform in COLS:
                self.df.at[i, platform] = True
        self.df.at[i, "Published At"] = pd.Timestamp.now()
        self._save()

    # ---------- save with colours ----------
    def _save(self):
        import xlsxwriter

        with pd.ExcelWriter(self.excel_path, engine="xlsxwriter") as writer:
            self.df.to_excel(writer, index=False, sheet_name="Sheet1")
            wb  = writer.book
            ws  = writer.sheets["Sheet1"]

            ws.freeze_panes(1, 0)      # 1. satırı freeze

            header_color = self.colors.get("header", "#D9E1F2")
            true_color   = self.colors.get("true",   "#C6EFCE")
            false_color  = self.colors.get("false",  "#FFC7CE")
            error_color  = self.colors.get("error",  "#FFB6C1")
            zebra_dark_c = self.colors.get("zebra_dark", "#E8E8E8")

            header_fmt = wb.add_format({"bold": True, "bg_color": header_color, "border": 1})
            true_fmt   = wb.add_format({"bg_color": true_color,   "border": 1})
            false_fmt  = wb.add_format({"bg_color": false_color,  "border": 1})
            error_fmt  = wb.add_format({"bg_color": error_color,  "border": 1})
            zebra_dark = wb.add_format({"bg_color": zebra_dark_c, "border": 1})
            zebra_light= wb.add_format({"border": 1})          # <-- eksik satır

            # kolon genişlikleri + header
            for col_num, col_name in enumerate(self.df.columns):
                max_len = max(self.df[col_name].astype(str).map(len).max(), len(col_name)) + 2
                ws.set_column(col_num, col_num, max_len)
                ws.write(0, col_num, col_name, header_fmt)

            # satır / hücre renklendirme
            for row_num, row in self.df.iterrows():
                fmt_base = zebra_dark if row_num % 2 else zebra_light
                for col_num, col in enumerate(self.df.columns):
                    val = row[col]
                    # string'e çevir (Path de olsa sorun yok)
                    val_str = str(val)

                    if isinstance(val, bool):
                        cell_fmt = true_fmt if val else false_fmt
                    elif val_str.upper() == "ERROR":
                        cell_fmt = error_fmt
                    else:
                        cell_fmt = fmt_base
                    ws.write(row_num + 1, col_num, val_str, cell_fmt)