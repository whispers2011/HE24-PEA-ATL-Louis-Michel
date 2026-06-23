from datetime import UTC, datetime

from app.models import Click
from app.services import stats


def test_summarize_empty_clicks():
    total, per_day = stats.summarize([])
    assert total == 0
    assert per_day == {}


def test_summarize_counts_total_and_groups_per_day():
    clicks = [
        Click(link_id=1, created_at=datetime(2026, 6, 1, 10, tzinfo=UTC)),
        Click(link_id=1, created_at=datetime(2026, 6, 1, 18, tzinfo=UTC)),
        Click(link_id=1, created_at=datetime(2026, 6, 2, 9, tzinfo=UTC)),
    ]
    total, per_day = stats.summarize(clicks)
    assert total == 3
    assert per_day == {"2026-06-01": 2, "2026-06-02": 1}
