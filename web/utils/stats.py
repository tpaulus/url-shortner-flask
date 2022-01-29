from datetime import timedelta, datetime
from typing import Dict

from models import Access


def generate_url_stats(slug: str) -> Dict[str, int]:
    now = datetime.utcnow()

    return {
        "last_day": Access.query.filter(Access.slug == slug, Access.access_date > now - timedelta(days=1)).count(),
        "last_week": Access.query.filter(Access.slug == slug, Access.access_date > now - timedelta(weeks=1)).count(),
        "all_time": Access.query.filter(Access.slug == slug).count()
    }
