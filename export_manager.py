import os, json
from typing import List
import pandas as pd
from .models import TrackingResult

class ExportManager:
    def __init__(self, out_dir: str, formats: list, excel_filename: str, csv_filename: str, json_filename: str):
        self.out_dir = out_dir
        self.formats = formats
        self.excel_filename = excel_filename
        self.csv_filename = csv_filename
        self.json_filename = json_filename
        os.makedirs(self.out_dir, exist_ok=True)

    def export(self, results: List[TrackingResult]):
        records = [r.model_dump() for r in results]
        df = pd.DataFrame(records)

        if "excel" in self.formats:
            df.to_excel(os.path.join(self.out_dir, self.excel_filename), index=False)

        if "csv" in self.formats:
            df.to_csv(os.path.join(self.out_dir, self.csv_filename), index=False)

        if "json" in self.formats:
            with open(os.path.join(self.out_dir, self.json_filename), "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
