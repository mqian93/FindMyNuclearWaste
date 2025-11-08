#Import Modules
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
from pathlib import Path

#Setup
DATA_DIR = Path("/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/data/shapefile")  # folder with shapefiles
N_POINTS = 100
OUTPUT_CSV = "random_bg_points_2024.csv"
zips = sorted(DATA_DIR.glob("tl_2024_*_bg.zip"))
if not zips:
    raise FileNotFoundError(f"No 'tl_2024_XX_bg.zip' files found in {DATA_DIR}")


# Read and concatenate shapefiles for all states
parts = []
for z in zips:
    # Each zip contains a shapefile; gpd.read_file can point at the zip directly
    parts.append(gpd.read_file(f"zip://{z}"))
bg = pd.concat(parts, ignore_index=True)
bg = gpd.GeoDataFrame(bg, geometry="geometry", crs=bg.crs)
bg = bg[~bg.geometry.is_empty & bg.geometry.notnull()].copy() #Drop empty


# Project lat and long data to an equal-area CRS 
# EPSG:2163 = US National Atlas Equal Area
bg_eq = bg.to_crs(2163)
areas = bg_eq.geometry.area.values

#Sampling probabilities uniform over land area
weights = np.where(np.isfinite(areas) & (areas > 0), areas, 0)
if weights.sum() == 0:
    raise ValueError()
probs = weights / weights.sum()

# Back to latitude/longitude
bg = bg.to_crs(4326)
geoms = bg.geometry.values

rng = np.random.default_rng(676767) #This is the seed we are using!!

##DEFINE FUNCTION FOR RANDOM SELECTION!!!!
def random_point_in_poly(poly):
    minx, miny, maxx, maxy = poly.bounds
    for _ in range(2000):
        x = rng.uniform(minx, maxx)
        y = rng.uniform(miny, maxy)
        p = Point(x, y)
        if poly.contains(p):
            return p
    # Fallback (rare): a guaranteed-inside point
    return poly.representative_point()

# First, choose polygons by area weight. Second, choose a point within each polygon
idxs = rng.choice(len(geoms), size=N_POINTS, p=probs, replace=True)
points = [random_point_in_poly(geoms[i]) for i in idxs]

#Output
lats = [p.y for p in points]
lons = [p.x for p in points]
df = pd.DataFrame({"latitude": lats, "longitude": lons})

#For validation only:
# # Print plain "lat, lon" lines
# for lat, lon in zip(lats, lons):
#     print(f"{lat:.6f}, {lon:.6f}")

# Save CSV
df.to_csv(OUTPUT_CSV, index=False)
