"""
Funciones para calcular niveles de riesgo de trafico y generar razonamientos.
"""

from datetime import datetime, date
from typing import List, Optional

from .schemas import AgendaEvent, WeatherHour, Holiday


def compute_score(
    target_date: date,
    agenda: List[AgendaEvent],
    weather: List[WeatherHour],
    holidays: List[Holiday],
    twitter_hits: int = 0,
) -> float:
    """
    Compute a numeric risk score for traffic given the signals for a specific date.
    """
    score = 0.0

    # Baseline by weekday (0=Monday..6=Sunday)
    weekday = target_date.weekday()
    baseline_map = {0: 0.8, 1: 0.6, 2: 0.8, 3: 1.0, 4: 2.0, 5: 0.4, 6: 0.2}
    score += baseline_map.get(weekday, 0.5)

    # Protest/manifestation effect
    for event in agenda:
        kind = (event.kind or "").lower()
        if kind in ("marcha", "concentración", "manifestación", "protesta"):
            attendance = event.expected_attendance or 0
            if attendance >= 1000:
                score += 1.0
            elif attendance >= 100:
                score += 0.6

    # Weather effect
    max_pop = max((hour.pop for hour in weather), default=0.0)
    max_wind = max((hour.wind_kph for hour in weather), default=0.0)
    if max_pop >= 0.7:
        score += 1.5
    elif max_pop >= 0.4:
        score += 1.0
    elif max_pop >= 0.2:
        score += 0.5
    if max_wind > 35.0:
        score += 0.3

    # Holiday effect (weekday bank/public holidays decrease traffic)
    is_public_weekday_holiday = any(h.type != "hebcal" and target_date.weekday() < 5 for h in holidays)
    if is_public_weekday_holiday:
        score -= 1.0

    # Twitter signal effect (reserved for future use)
    if twitter_hits >= 10:
        score += 0.8
    elif twitter_hits >= 3:
        score += 0.5

    return score


def map_score_to_level(score: float) -> str:
    """
    Convert a numeric score into one of five categorical levels in Spanish.
    """
    if score <= 1.0:
        return "Bajo"
    elif score <= 2.0:
        return "Medio"
    elif score <= 3.0:
        return "Alto"
    elif score <= 4.0:
        return "Muy alto"
    else:
        return "Extremo"


def generate_reasoning(
    target_date: date,
    agenda: List[AgendaEvent],
    weather: List[WeatherHour],
    holidays: List[Holiday],
    score: float,
) -> List[str]:
    """
    Generate human-friendly reasoning strings (in Spanish) explaining why a certain level was assigned.
    """
    reasons: List[str] = []

    # Day-of-week reasoning
    weekday = target_date.weekday()
    if weekday == 4:
        reasons.append("Es viernes, lo que suele incrementar el tráfico de regreso a casa.")
    elif weekday == 3:
        reasons.append("Es jueves, con un efecto moderado en el tráfico laboral.")
    elif weekday in (5, 6):
        reasons.append("Es fin de semana, cuando suele haber menos tráfico laboral.")

    # Protest reasoning
    protest_events = [e for e in agenda if (e.kind or "").lower() in ("marcha", "concentración", "manifestación", "protesta")]
    if protest_events:
        count = len(protest_events)
        reasons.append(
            f"Se encontraron {count} protestas o manifestaciones programadas que pueden afectar la movilidad."
        )

    # Weather reasoning
    max_pop = max((hour.pop for hour in weather), default=0.0)
    if max_pop >= 0.4:
        reasons.append("Hay probabilidad de lluvia, lo que aumenta el tráfico.")

    # Holiday reasoning
    is_public_weekday_holiday = any(h.type != "hebcal" and target_date.weekday() < 5 for h in holidays)
    if is_public_weekday_holiday:
        reasons.append("Hay un día festivo, lo que podría reducir el tráfico laboral.")

    return reasons
