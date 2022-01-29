import datetime
from typing import Optional
from uuid import uuid4

from app import db
from constants import SLUG_LENGTH


class ShortUrl(db.Model):
    __tablename__ = 'urls'

    slug = db.Column(db.String(length=SLUG_LENGTH), primary_key=True, unique=True)
    url = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    expires = db.Column(db.DateTime)

    def __init__(self, slug: str, url: str, expiry_delta: Optional[datetime.timedelta]):
        self.slug = slug
        self.url = url
        self.date_created = datetime.datetime.now()
        self.expires = (self.date_created + expiry_delta) if expiry_delta else None


class Access(db.Model):
    __tablename__ = 'access'

    event_id = db.Column(db.String(length=36), primary_key=True)  # UUIDs are 36 characters long
    slug = db.Column(db.String(length=SLUG_LENGTH), db.ForeignKey(ShortUrl.slug), nullable=False)
    access_date = db.Column(db.DateTime, nullable=False)
    source_ip = db.Column(db.String)
    source_user_agent = db.Column(db.String)

    def __init__(self, slug: str, source_ip: Optional[str] = None, source_user_agent: Optional[str] = None):
        self.event_id = str(uuid4())
        self.slug = slug
        self.access_date = datetime.datetime.now()
        self.source_ip = source_ip
        self.source_user_agent = source_user_agent
