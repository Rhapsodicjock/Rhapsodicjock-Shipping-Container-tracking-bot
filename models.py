from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class ContainerQuery(BaseModel):
    container_no: str
    carrier: str
    booking_no: Optional[str] = None

class TrackingResult(BaseModel):
    container_no: str
    carrier: str
    status: str = "UNKNOWN"
    last_location: Optional[str] = None
    eta: Optional[str] = None
    raw: Optional[Dict] = None
    success: bool = False
    error: Optional[str] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
