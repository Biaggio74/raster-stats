from shapely.geometry import shape, Point, Polygon
import numpy as np
import geog
import rasterio
import rasterstats as rs
import geopandas as pd
from geopandas import GeoSeries

def buffer(features, buffer=1.0):
    """Buffer a feature by specified units
    """
    for feature in features:
        geom = shape(feature['geometry']) # Convert to shapely geometry to operate on it
        geom = geom.buffer(buffer) # Buffer
        new_feature = feature.copy()
        new_feature['geometry'] = geom.__geo_interface__
        yield new_feature

def test_geo(lat, lon, radius):
    coordinates = Point(float(lon),float(lat))
    coordinates = coordinates.__geo_interface__
    return {'lat': lat,
            'lon': lon,
            'radius': radius,
            'shapely': coordinates}

def polygons(lat, lon, radius):
    FILE = 'https://s3.eu-central-1.amazonaws.com/standarise/GlobeCover/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1.0.tif'
    #specify the whole 360deg polygon shape
    coordinates = Point(float(lon),float(lat))
    angle = 45 #is one sector
    sides = 8 #the number of sides of the polygon per sector
    num_sectors = 8

    #Creating the 8 sectors
    #Numbering goes from 1 to 8, 1 is 0 to 45deg, 2 is 45 to 90deg, etc.
    def create_sectors(coords, radius, sides, start, angle):
        center = np.array(coords)
        angles = np.linspace(start, angle, sides + 1 )
        polygon = geog.propagate(coords, angles, radius, bearing=True) #facing true north
        polygonArr = np.append([center], polygon, axis=0)
        return polygonArr

    sector_array = {}
    for i in range(num_sectors):
        sector_array[i+1] = create_sectors(coordinates, float(radius), sides, i*360/num_sectors, (i+1)*360/num_sectors)

    return sector_array[1]
