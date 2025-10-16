import sys
import numpy as np
import geopandas as gpd
import rasterio
import overpass
import osm2geojson
import codecs
from geocube.api.core import make_geocube
import pandas as pd
if sys.argv[1]=='--help':
    print('''python3 osm2raster.py radius lat lng pixel-size''')
else:
    #------------------------------------
    api = overpass.API()
    radius=int(sys.argv[1])
    #------------------------------------
    response = api.get('nwr["building"](around:'+str(radius*2)+','+str(sys.argv[2])+','+str(sys.argv[3])+');out geom;', responseformat="xml")
    with open("input.osm", "w") as text_file:
        text_file.write(str(response))
    print('downloaded and written to input.osm')
    with codecs.open('input.osm', 'r', encoding='utf-8') as data:
        xml = data.read()

    geojson = osm2geojson.xml2geojson(xml, filter_used_refs=False, log_level='INFO')
    print('load geojson sucessfully')
    #------------------------------------
    gdf=gpd.GeoDataFrame.from_features(geojson,crs='EPSG:4326').to_crs('EPSG:3857')
    df=pd.DataFrame({'building':[0],'lat':[sys.argv[2]],'lng':[sys.argv[3]]})
    extent=gpd.GeoDataFrame(geometry=gpd.GeoSeries(gpd.points_from_xy(df.lng,df.lat),crs='EPSG:4326').to_crs('EPSG:3857').buffer(radius))
    gdf['building']=1
    extent['building']=0
    gdf=gpd.clip(gdf,extent)
    gdf=pd.concat([extent,gdf],ignore_index=True)
    print(gdf)
    print('done converting to GeoDataFrame in CRS EPSG:3857')
    gdf.to_file('geom.gpkg',driver='GPKG')
    #------------------------------------
    cube = make_geocube(
        gdf,
        measurements=["building"],
        resolution=(float(sys.argv[4]), -float(sys.argv[4])),
        fill=0
        )
    cube.building.rio.to_raster('geom.tif')
    grid=cube.building.to_numpy()
    grid=np.flip(np.flip(grid,0),1) #correct direction
    np.save('map_grid.npy',grid)
