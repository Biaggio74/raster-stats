from flask import Flask, jsonify
from raster_stats import sector_raster_stats as rstats
from polygon import test_geo, polygons
#import jsonify
app = Flask(__name__)

@app.route('/test')
def tes_page():
    return '<h1>Test page</h1>'

@app.route('/stats')
def stats():
    stats = rstats(-6.2, 38, 1500)
    return jsonify(stats)

@app.route('/testgeo')
def geo():
    geom = test_geo(-6,35,1200)
    return jsonify(geom)

@app.route('/polygons')
def polygon():
    geom = polygons(-6,35,1200)
    response = {
                'data': geom,
                'err': ''
        }

    return jsonify(response)


if __name__ == '__main__':
    app.run()
