import datetime
import json
import re

import dateutil.parser
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

from .config import Config
from .plotting import make_map, get_quake_feats


def create_app():
    """Create and configure and instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def home():
        # return render_template('index.html')
        return redirect(url_for('map'))

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/markets')
    def markets():
        return render_template('markets.html')

    @app.route("/gold", methods = ["POST"])
    def gold():
        return render_template('gold.html')

    @app.route("/sp500", methods = ["POST"])
    def sp500():
        return render_template('sp500.html')

    @app.route("/intermarket", methods = ["POST"])
    def intermarket():
        return render_template('intermarket.html')

    @app.route("/marketmodels", methods = ["POST"])
    def marketmodels():
        return render_template('marketmodels.html')

    @app.route('/damage')
    def damage():
        return render_template('damage.html')

    @app.route('/map', methods=['GET', 'POST'])
    def map():
        dt_end = datetime.datetime.utcnow()
        dt_beg = (dt_end - datetime.timedelta(days=30)).isoformat()
        dt_end = dt_end.isoformat()

        qry_params = {}
        try:
            qry_params['starttime'] = parse_dtstr(
                request.values.get('starttime', dt_beg))
            qry_params['endtime'] = parse_dtstr(
                request.values.get('endtime', dt_end))
        except ValueError:
            qry_params['starttime'] = parse_dtstr(dt_beg)
            qry_params['endtime'] = parse_dtstr(dt_end)
            pass  # TODO: flash message "Invalid Date, reverted to defaults"
        
        qry_params['minmagnitude'] = request.values.get('minmagnitude', '2.5')
        
        map_params = {}
        map_params['period_amt'] = request.values.get('period_amt', '6')
        map_params['period_unit'] = request.values.get('period_unit', 'Hours')
        
        t_prefix = 'T' if map_params['period_unit'] == 'Hours' else ''
        
        map_params['period'] = ('P' + t_prefix + map_params['period_amt'] + 
                                map_params['period_unit'][0])

        duration = int(map_params['period_amt']) * 2
        map_params['duration'] = re.sub(r'\d+', str(duration), 
                                        map_params['period'])

        # get quake geojson
        quake_feats = get_quake_feats(qry_params)

        # add faults
        with open("data/PB2002_boundaries.json", "r") as read_file:
            fault_feats = json.load(read_file)
        
        fault_feats = {
            'type': 'FeatureCollection',
            'features': fault_feats['features'],
        }

        return render_template('map.html', qry_params=qry_params, 
                               map_params=map_params, fault_feats=fault_feats,
                               quake_feats=quake_feats)

    @app.route('/earthquakes.html')
    def earthquakes():
        return render_template('earthquakes.html')
    
    @app.errorhandler(404) 
    def not_found(e):
        return render_template("404.html") 

    return app


def parse_dtstr(dtstr):
    return dateutil.parser.parse(dtstr).strftime("%Y-%m-%d %H:%M")
