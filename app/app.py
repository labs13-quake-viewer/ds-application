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

    @app.route('/map', methods=['GET', 'POST'])
    def map():
        if request.method == 'POST':
            params = {}
            params['startdate'] = request.form.get('startdate')
            params['startdate'] = request.form.get('enddate')
            params['minmagnitude'] = request.form.get('minmagnitude', '2.5')
        else:
            params = request.args.to_dict()
            params['minmagnitude'] = params.get('minmagnitude', '2.5')

        make_map(payload=params)
        return render_template('map.html')

    @app.route('/earthquakes.html')
    def earthquakes():
        return render_template('earthquakes.html')

    return app
