"""
FastAPI application para CDMX Predictor de Tráfico.
"""

from datetime import date
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .data_fetchers import fetch_agenda, fetch_weather, fetch_holidays
from .scoring import compute_score, map_score_to_level, generate_reasoning
from .schemas import PredictionResponse, EvidenceResponse, EvidenceItem

app = FastAPI(title="CDMX Predictor de Tráfico", version="0.1.0")

# Configurar CORS para permitir acceso desde cualquier origen (para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/v1/predict", response_model=PredictionResponse)
async def predict(
    date: date = Query(..., description="Fecha objetivo (YYYY-MM-DD)"),
    city: str = Query("cdmx", description="Ciudad para la predicción"),
):
    """
    Endpoint principal para obtener el nivel de tráfico.
    """
    agenda = await fetch_agenda(date)
    weather = await fetch_weather(date)
    holidays = await fetch_holidays(date)

    score = compute_score(date, agenda, weather, holidays)
    level = map_score_to_level(score)
    reasons = generate_reasoning(date, agenda, weather, holidays, score)

    # Ventanas pico predeterminadas (ajustadas por eventos y clima en futuras versiones)
    peak_hours = ["07:00-10:00", "15:00-19:00"]

    # Construir evidencias a partir de la agenda
    evidence_items: List[EvidenceItem] = []
    for event in agenda:
        evidence_items.append(
            EvidenceItem(
                type="agenda",
                title=event.kind or "evento",
                url=event.source or "",
                pages=event.pages or [],
            )
        )

    return PredictionResponse(
        date=date,
        city=city,
        level=level,
        prob=None,
        peak_hours=peak_hours,
        reasons=reasons,
        evidence=evidence_items,
    )


@app.get("/v1/evidence", response_model=EvidenceResponse)
async def get_evidence(
    date: date = Query(..., description="Fecha objetivo (YYYY-MM-DD)"),
    city: str = Query("cdmx", description="Ciudad para la predicción"),
):
    """
    Devuelve la lista de evidencias usadas para la predicción.
    """
    agenda = await fetch_agenda(date)
    weather = await fetch_weather(date)
    holidays = await fetch_holidays(date)

    evidence_items: List[EvidenceItem] = []
    for event in agenda:
        evidence_items.append(
            EvidenceItem(
                type="agenda",
                title=event.kind or "evento",
                url=event.source or "",
                pages=event.pages or [],
            )
        )

    return EvidenceResponse(
        date=date,
        city=city,
        evidence=evidence_items,
    )


@app.get("/v1/healthz")
async def healthz():
    """
    Endpoint de salud.
    """
    return {"status": "ok"}
