from typing import Dict, Any
from .models import TrackingResult

def parse_result(container_no: str, carrier: str, raw: Dict[str, Any]) -> TrackingResult:
    # Map raw dict to normalized fields
    status = raw.get("status", "UNKNOWN")
    last_loc = raw.get("last_location")
    eta = raw.get("eta")
    return TrackingResult(
        container_no=container_no,
        carrier=carrier,
        status=status,
        last_location=last_loc,
        eta=eta,
        raw=raw,
        success=raw.get("success", False),
        error=raw.get("error"),
    )
