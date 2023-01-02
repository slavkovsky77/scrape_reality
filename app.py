import flask
import flask_assets

from flask import Blueprint, render_template
from scrapper.db import Database
from scrapper.real_estate_scrapper import scrap_flats

bp = Blueprint('scrap_reality', __name__)

@bp.route('/')
def index():
    db = Database()
    return render_template(
        'index.html',
        flats=db.load_flats()
    )


def create_app():
    app = flask.Flask(__name__)
    assets = flask_assets.Environment()
    assets.init_app(app)
    scrap_flats()
    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint='index')
    return app

app = create_app()

if __name__ == "__main__":
    app.run()
