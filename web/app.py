# app.py


from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/slug", methods=['PUT'])
def create_short_url():
    return "Hi!"


@app.route("/slug/<slug>", methods=['DELETE'])
def delete_short_url(slug: str):
    return f"Bye {slug}!"


@app.route("/slug/<slug>", methods=['GET'])
def describe_short_url(slug: str):
    return f"My name is {slug}!"


@app.route("/<slug>", methods=['GET'])
def expand_url(slug: str):
    return f"Hello {slug}!"


if __name__ == '__main__':
    app.run()
