from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import BaseConfig

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    db.init_app(app)

    # This is a local import to deal with circular dependencies with the "db"
    from controller.apis import index, delete_short_url, create_short_url, describe_short_url, expand_url

    app.add_url_rule("/", "index", index, methods=["GET", "POST"])
    app.add_url_rule("/slug", "create_short_url", create_short_url, methods=["PUT"])
    app.add_url_rule("/slugs/<slug>", "delete_short_url", delete_short_url, methods=["DELETE"])
    app.add_url_rule("/slugs/<slug>", "describe_short_url", describe_short_url, methods=["GET"])
    app.add_url_rule("/<slug>", "expand_url", expand_url, methods=["GET"])

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
