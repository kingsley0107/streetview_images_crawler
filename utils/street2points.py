import geopandas as gpd
import pandas as pd
from tqdm import tqdm


def generate_streetview_points(road_gdf, threshold=50):
    road_gdf = road_gdf.to_crs("epsg:3857")
    road_gdf["total_length"] = road_gdf.geometry.length
    png_lst = []
    for index, row in tqdm(road_gdf.iterrows(), total=road_gdf.shape[0]):
        selected_line_geom = row["geometry"]
        selected_length = selected_line_geom.length
        slices = round(selected_length / threshold)
        splitted_list = [
            selected_line_geom.interpolate((i / slices), normalized=True)
            for i in range(1, slices)
        ]
        png_lst.extend(splitted_list)
    pnt_df = pd.DataFrame(png_lst, columns=["geometry"])
    pnt_gdf = gpd.GeoDataFrame(pnt_df, geometry="geometry", crs=road_gdf.crs)
    pnt_gdf = pnt_gdf.to_crs("epsg:4326")
    return pnt_gdf
