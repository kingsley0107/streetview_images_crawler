import geopandas as gpd
import pandas as pd
from schedule.schedule import SVI_crawler
from config.config import recorder
from utils.street2points import generate_streetview_points


def points_from_road(road_path, threshold=100):
    """_summary_

    Args:
        road_path (_type_): _road_path
        threshold (int, optional): _split road in threshold meters_. Defaults to 100.

    Returns:
        _type_: _description_
    """
    road = gpd.read_file(road_path).to_crs("epsg:4326")
    pnts = generate_streetview_points(road, threshold)
    return pnts


def run(pnts, recorder):
    recorder = SVI_crawler(pnts, recorder)
    recorder.to_excel(r"./dir/crawl_recorder.xlsx")


if __name__ == "__main__":
    # 如果是路网生成点 用这两行代码生成Pnts
    road_path = r"./dir/shp/road.shp"
    pnts = points_from_road(road_path, 50)
    pnts.to_file(r"./data/pts.geojson")
    # 如果直接有点数据，那么直接如下读取点就好了
    # pnts = gpd.read_file(r'...')

    run(pnts, recorder)
