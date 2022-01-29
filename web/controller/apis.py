import logging
from datetime import timedelta, datetime
from typing import Optional, Union, Dict

from flask import render_template, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app import db
from constants import VALID_TIME_UNITS, MAX_SLUG_GENERATION_ATTEMPTS
from models import ShortUrl, Access
from utils.slug_generator import generate_slug
from utils.stats import generate_url_stats

log = logging.getLogger(__name__)


# Routes are registered in app:create_app
def index():
    return render_template('index.html')


def create_short_url():
    long_url: Optional[str] = request.json.get("long_url")
    expires: Optional[Dict[str, Union[str, int]]] = request.json.get("expires")

    # TODO Support Custom Aliases (and check it against the reserved list)

    if not long_url:
        log.info("No Long URL Present in the request")
        abort(400)  # 400 - Bad Request

    if expires:
        if any(key not in VALID_TIME_UNITS for key in expires):
            log.info("Invalid Expiry Time Unit")
            abort(400)  # 400 - Bad Request

        if any(not isinstance(value, int) or value <= 0 for value in expires.values()):
            log.info("Value is not a positive integer")
            abort(400)  # 400 - Bad Request

        expiry_time_delta: Optional[timedelta] = timedelta(**expires)
    else:
        expiry_time_delta = None

    session: Session = db.session
    attempt: int = 0
    while attempt < MAX_SLUG_GENERATION_ATTEMPTS:
        # Generate Short URL
        proposed_slug: str = generate_slug()

        # Insert into DB
        session.add(ShortUrl(proposed_slug, long_url, expiry_time_delta))
        try:
            session.commit()
        except IntegrityError:
            log.warning(f"Slug Collision, will attempt {3 - MAX_SLUG_GENERATION_ATTEMPTS} more times")
            attempt += 1
            continue
            # TODO Log Metric that there was a slug collision

        return {"slug": proposed_slug,
                "short_url": f"{request.host}/{proposed_slug}"}

    log.error("Unable to shorten URL")
    abort(500)  # 500 - Internal Error


def delete_short_url(slug: str):
    short_url: Optional[ShortUrl] = ShortUrl.query.get_or_404({"slug": slug})

    session: Session = db.session
    for record in Access.query.filter(Access.slug == slug).all():
        session.delete(record)
    session.delete(short_url)
    session.commit()

    return f"Deleted {slug}"


def describe_short_url(slug: str):
    if not slug:
        abort(400)  # 400 - Bad Request

    short_url: ShortUrl = ShortUrl.query.get_or_404({"slug": slug})

    return {
        "slug": short_url.slug,
        "long_url": short_url.url,
        "date_created": short_url.date_created,
        "expires": short_url.expires,
        "expired": short_url.expires and short_url.expires < datetime.utcnow(),
        "stats": generate_url_stats(slug)
    }


def expand_url(slug: str):
    short_url: ShortUrl = ShortUrl.query.get_or_404({"slug": slug})

    if short_url.expires and short_url.expires < datetime.utcnow():
        log.info(f"Received request to expand {slug}, but it has expired.")
        abort(410)  # 410 - Gone

    # Log Access
    session: Session = db.session
    session.add(Access(slug, request.remote_addr, request.user_agent.string))
    session.commit()

    return redirect(short_url.url)
