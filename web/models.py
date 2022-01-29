import datetime
from uuid import uuid4

from app import db
from constants import SLUG_LENGTH


class ShortUrl(db.Model):
    __tablename__ = 'urls'

    slug = db.Column(db.String(length=SLUG_LENGTH), primary_key=True, unique=True)
    url = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, slug: str, url: str):
        self.slug = slug
        self.url = url
        self.date_created = datetime.datetime.now()


class Access(db.Model):
    __tablename__ = 'access'

    event_id = db.Column(db.String(length=36), primary_key=True)  # UUIDs are 36 characters long
    slug = db.Column(db.String(length=SLUG_LENGTH), db.ForeignKey(ShortUrl.slug), nullable=False)
    access_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, slug: str):
        self.event_id = str(uuid4())
        self.slug = slug
        self.access_date = datetime.datetime.now()
