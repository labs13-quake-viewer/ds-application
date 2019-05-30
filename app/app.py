import pandas as pd
from flask import Flask, request, render_template

from .config import Config
from .plotting import make_map

def create_app():
    """Create and configure and instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def root():
        make_map()
        return render_template('earthquakes.html')

    return app
