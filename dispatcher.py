from typing import Dict, Type
from .carriers.base import BaseCarrier
from .carriers.msc import MSCCarrier
from .carriers.pil import PILCarrier
from .carriers.maersk import MaerskCarrier

CARRIER_MAP: Dict[str, Type[BaseCarrier]] = {
    "MSC": MSCCarrier,
    "PIL": PILCarrier,
    "Maersk": MaerskCarrier,
}

def get_carrier(name: str) -> Type[BaseCarrier]:
    key = name.strip()
    if key not in CARRIER_MAP:
        raise ValueError(f"Unsupported carrier: {name}")
    return CARRIER_MAP[key]
