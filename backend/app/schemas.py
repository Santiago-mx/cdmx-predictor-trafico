from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel


class EvidenceItem(BaseModel):
    type: str
    title: Optional[str] = None
    url: Optional[str] = None
    when: Optional[str] = None
    metric: Optional[str] = None


class PredictionResponse(BaseModel):
    date: date
    level: str
    score: float
    peak_hours: List[str]
    reasons: List[str]
    evidence: List[EvidenceItem]


class AgendaEvent(BaseModel):
    kind: str
    expected_attendance: int
    start_ts: Optional[datetime] = None
    end_ts: Optional[datetime] = None
    description: Optional[str] = None
    source_url: Optional[str] = None


class WeatherHour(BaseModel):
    hour: int
    pop: float
    rain_mm: float = 0.0
    wind_kph: float = 0.0


class Holiday(BaseModel):
    name: str
    type: str
    source: str


class EvidenceResponse(BaseModel):
    date: date
    agenda: List[AgendaEvent]
    weather: List[WeatherHour]
    holidays: List[Holiday]
