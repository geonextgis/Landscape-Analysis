import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import os
from glob import glob
import pylandstats as pls
from concurrent.futures import ProcessPoolExecutor

import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams['font.serif'] = 'Times New Roman'

data_dir = r'/beegfs/halder/jupyter_playgroundnoconda_p3.12_1/jupyter_work/project/DATA'
out_dir = r'/beegfs/halder/GITHUB/Landscape-Analysis/data'


# Read the exported data
lulc_file_path = os.path.join(out_dir, 'raster', 'ESA_WorldCover_2021_DE_EPSG_25832.tif')


grids_gdf = gpd.read_file(os.path.join(out_dir, 'vector', 'DE_Hexbins_5sqkm.shp'))
grids_gdf = grids_gdf.to_crs('EPSG:25832')
grids_gdf = grids_gdf[['id', 'geometry']]
grids_gdf['id'] = grids_gdf['id'].astype(int)


# Read the LULC using PyLandStats package
za = pls.ZonalAnalysis(lulc_file_path, zones=grids_gdf, zone_index='id', zone_nodata=0, neighborhood_rule=8)
# Extract all the class metrics
class_metrics_df = za.compute_class_metrics_df().reset_index()
# Extract the landscape metrics
landscape_metrics_df = za.compute_landscape_metrics_df().reset_index()


# Save the dataframes
class_metrics_df.to_csv(os.path.join(out_dir, 'output', 'Landscape_Metrics', 'class_metrics.csv'), index=False)
landscape_metrics_df.to_csv(os.path.join(out_dir, 'output', 'Landscape_Metrics', 'landscape_metrics.csv'), index=False)

