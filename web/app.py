from typing import Optional

from flask import Flask
from flask import request, render_template, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import BaseConfig
from utils.slug_generator import generate_slug

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

# DAOs MUST be imported after the DB is declared
from models import ShortUrl, Access


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/slug", methods=['PUT'])
def create_short_url():
    long_url = request.json.get("long_url")

    if not long_url:
        abort(400)  # 400 - Bad Request

    session: Session = db.session
    attempt: int = 0
    while attempt < 3:
        # Generate Short URL
        proposed_slug: str = generate_slug()

        # Insert into DB
        session.add(ShortUrl(proposed_slug, long_url))
        try:
            session.commit()
        except IntegrityError:
            attempt += 1
            continue
            # TODO Log Metric that there was a slug collision

        return {"slug": proposed_slug,
                "short_url": f"{request.host}/{proposed_slug}"}

    abort(500)  # 500 - Internal Error


@app.route("/slug/<slug>", methods=['DELETE'])
def delete_short_url(slug: str):
    short_url: Optional[ShortUrl] = ShortUrl.query.get_or_404({"slug": slug})

    session: Session = db.session
    session.delete(short_url)
    session.commit()

    return f"Deleted {slug}"


@app.route("/slug/<slug>", methods=['GET'])
def describe_short_url(slug: str):
    if not slug:
        abort(400)  # 400 - Bad Request

    short_url: Optional[ShortUrl] = ShortUrl.query.get_or_404({"slug": slug})

    return {
        "slug": short_url.slug,
        "long_url": short_url.url,
        "date_created": short_url.date_created,
    }


@app.route("/<slug>", methods=['GET'])
def expand_url(slug: str):
    short_url: Optional[ShortUrl] = ShortUrl.query.get_or_404({"slug": slug})

    # Log Access
    session: Session = db.session
    session.add(Access(slug))
    session.commit()

    return redirect(short_url.url)


if __name__ == '__main__':
    app.run()
