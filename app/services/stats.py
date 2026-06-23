"""Aggregation der Klick-Statistik eines Kurzlinks."""

from collections import Counter

from app.models import Click


def summarize(clicks: list[Click]) -> tuple[int, dict[str, int]]:
    """Liefert die Gesamtzahl und die Klicks pro Tag (ISO-Datum, sortiert)."""
    per_day = Counter(click.created_at.date().isoformat() for click in clicks)
    return len(clicks), dict(sorted(per_day.items()))
