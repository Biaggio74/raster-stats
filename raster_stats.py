from geopandas import GeoSeries
import geopandas as pd
from shapely.geometry import Point, Polygon
#from shapely.geometry import point
import numpy as np
import geog
import rasterio
#import matplotlib.pyplot as plt
#import rasterio.plot as rioplot
import rasterstats as rs

BoundingBox = {'left':-18.619444444805282, 'bottom': -35.32207072412766, 'right':51.911321709874414, 'top': 37.840407079223375}

def sector_raster_stats(lat, lon, radius):
    if float(lon) > BoundingBox['left'] and float(lon) < BoundingBox['right'] and float(lat) < BoundingBox['top'] and float(lat) > BoundingBox['bottom']:
        #Lets return the expected raster data
        #Main asset
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

        #At this point the polygon should be reprojected to the cordinate system of the raster file
        #Since rasterstats does not deal with it
        #Or the raster file into WGS84
        geo_series = []
        for p in range(num_sectors):
            geo_series.append(Polygon(sector_array[p+1]))
        features = GeoSeries(geo_series)

        #Read the raster file as window with rasterio
        with rasterio.open(FILE) as src:
            x, y = src.index(coordinates.x, coordinates.y)
            #w = src.read(1, window=((x-1*256, x + 1*256),(y-1*256, y + 1*256)))
            sector_stats = rs.zonal_stats(features, FILE, prefix='land_type_',
                                          stats="min max median majority sum",
                                          categorical=True,
                                          all_touched=True,
                                          geojson_out=True)
        return sector_stats
    else:
        return {'error': 'Coordinates are not in the boundingbox',
               'BoundingBox': src.bounds}
