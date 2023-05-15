import flask
import flask_assets
import scrapper.api
import json
import re

from flask import Blueprint, render_template
from scrapper.api import get_flats
from scrapper.db import Database

bp = Blueprint('scrap_reality', __name__)


@bp.route('/')
def index():
    response = get_flats()
    flats = json.loads(response.data.decode('utf-8'))
    apartment_numbers = [flat['apartment_number'] for flat in flats]
    clean_apartment_numbers = [
        re.sub(r'[^a-zA-Z0-9]', '', flat['apartment_number'])
        for flat in flats]

    return render_template(
        'index.html',
        apartment_numbers=apartment_numbers,
        clean_apartment_numbers=clean_apartment_numbers,
        flats=flats,
        zip=zip
    )


def create_app():
    app = flask.Flask(__name__)
    assets = flask_assets.Environment()
    assets.init_app(app)

    app.register_blueprint(scrapper.api.bp)
    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint='index')
    db = Database()
    db.create()

    @app.add_template_filter
    def jsonify(data):
        return json.dumps(data)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
