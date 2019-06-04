import pandas as pd
from flask import Flask, request, render_template

from .config import Config
from .plotting import make_map

def create_app():
    """Create and configure and instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/map')
    def map():
        return render_template('map.html')

    @app.route('/earthquakes')
    def earthquakes():
        all_args = request.args.to_dict()
        all_args['minmagnitude'] = all_args.get('minmagnitude', '2.5')
        make_map(payload=all_args)
        return render_template('earthquakes.html')

    return app
