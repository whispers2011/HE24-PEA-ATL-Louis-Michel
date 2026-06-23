"""Klick-Statistik eines eigenen Kurzlinks."""

from fastapi import APIRouter, Depends

from app.models import Link
from app.routers.links import get_owned_link
from app.schemas import StatsRead
from app.services import stats

router = APIRouter(prefix="/api/links", tags=["stats"])


@router.get("/{code}/stats", response_model=StatsRead)
def link_stats(link: Link = Depends(get_owned_link)) -> StatsRead:
    """Liefert Gesamt- und Tagesstatistik der Klicks eines eigenen Links."""
    total, per_day = stats.summarize(link.clicks)
    return StatsRead(code=link.code, total=total, per_day=per_day)
