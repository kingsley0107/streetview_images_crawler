from config.config import FEATURE_YEAR
import pandas as pd
import geopandas as gpd
from spider.crawler import GSV_Crawler

if __name__ == "__main__":
    Crawler = GSV_Crawler()
    accident = pd.read_csv(r'./2022_accident.csv')[['Easting',
                                                    'Northing']].head(10)
    accident['geometry'] = gpd.points_from_xy(
        accident["Easting"], accident["Northing"],
        crs="epsg:27700").to_crs("epsg:4326")
    accident['GSV_ID'] = accident['geometry'].apply(
        lambda x: Crawler.get_SVI(Crawler.get_panoid(x)))
    accident.to_csv(rf"./{FEATURE_YEAR}_GSV/recorder.csv")
