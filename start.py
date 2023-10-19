from config.config import FEATURE_YEAR
import pandas as pd
import geopandas as gpd
from spider.crawler import GSV_Crawler
from tqdm import tqdm

tqdm.pandas(desc='pandas bar')
if __name__ == "__main__":
    Crawler = GSV_Crawler()
    accident = pd.read_csv(r'./2022_accident.csv')[[
        '_Collision Id', 'Easting', 'Northing'
    ]]
    accident_unique = accident.drop_duplicates(['_Collision Id'])
    accident['geometry'] = gpd.points_from_xy(
        accident["Easting"], accident["Northing"],
        crs="epsg:27700").to_crs("epsg:4326")
    accident['GSV_ID'] = accident['geometry'].progress_apply(
        lambda x: Crawler.get_SVI(Crawler.get_panoid(x)))
    recorder = accident[['_Collision Id', 'GSV_ID']]
    recorder.to_csv(rf"./{FEATURE_YEAR}_GSV/recorder.csv")
