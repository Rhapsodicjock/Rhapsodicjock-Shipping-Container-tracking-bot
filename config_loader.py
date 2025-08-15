import yaml
from typing import List
import pandas as pd
from pydantic import BaseModel
from .models import ContainerQuery

class AppConfig(BaseModel):
    settings: dict
    export: dict
    carriers: list
    inputs: dict

def load_config(path: str) -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)

def load_containers(cfg: AppConfig) -> List[ContainerQuery]:
    items = []
    inputs = cfg.inputs or {}
    if "containers" in inputs and inputs["containers"]:
        for row in inputs["containers"]:
            items.append(ContainerQuery(**row))
        return items
    # else load from excel
    excel = inputs.get("excel_path")
    sheet = inputs.get("sheet_name", 0)
    df = pd.read_excel(excel, sheet_name=sheet)
    for _, r in df.iterrows():
        items.append(ContainerQuery(container_no=str(r["container_no"]), carrier=str(r["carrier"])))
    return items
