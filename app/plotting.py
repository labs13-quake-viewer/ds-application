import json
from io import StringIO

import folium
import pandas as pd
import requests
from folium import plugins


def make_map(save_path='app/templates/earthquakes.html', payload={}):
    payload['format'] = 'csv'
    r = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query', 
                     params=payload)

    df = pd.read_csv(StringIO(r.text))

    features = [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [r['longitude'], r['latitude']],
            },
            'properties': {
                'time': r['time'][0:-1],
                'popup': (
                    f"<strong>Time:</strong> {r['time']}<br>"
                    f"<strong>Place:</strong> {r['place']}<br>"
                    f"<strong>Magnitude:</strong> {r['mag']} {r['magType']}<br>"
                    f"<strong>Depth:</strong> {r['depth']}<br>"
                ),
                'icon': 'circle',
                'iconstyle': {
                    'fillOpacity': 0.5,
                    'stroke': 0,
                    'radius': r['mag'] * 2.5
                },
            }
        } for i, r in df.iterrows()
    ]

    m = folium.Map(
        tiles='CartoDBpositron',
    #     zoom_start=1,
    #     no_wrap=True,
        min_zoom=1.5,
        max_zoom=5,
    )

    # add faults
    with open("data/PB2002_boundaries.json", "r") as read_file:
        fault_features = json.load(read_file)
    
    folium.GeoJson(
        {
            'type': 'FeatureCollection',
            'features': fault_features['features'],
        },
        style_function = lambda x: {
            'color': 'red',
            'weight': 0.5,
        }
    ).add_to(m)

    plugins.TimestampedGeoJson(
        {
            'type': 'FeatureCollection',
            'features': features
        },
        period='PT6H', # six hour
        time_slider_drag_update=True,
        duration='PT12H',
        date_options='YYYY-MM-DD HH UTC'
    ).add_to(m)

    folium.plugins.Fullscreen(
        position='topright',
        force_separate_button=True,
    ).add_to(m)

    m.save(save_path)
