import geopandas as gpd
import pandas as pd
from schedule.schedule import SVI_crawler
from config.config import recorder
from utils.street2points import generate_streetview_points


def points_from_road(road_path, threshold=100):
    road = gpd.read_file(road_path)
    pnts = generate_streetview_points(road, threshold)
    return pnts


def run(pnts, recorder):
    recorder = SVI_crawler(pnts, recorder)
    recorder.to_excel(r"./dir/crawl_recorder.xlsx")


if __name__ == "__main__":
    # 如果是路网生成点 用这两行代码生成Pnts
    road_path = r"./dir/shp/road.shp"
    pnts = points_from_road(road_path)

    # 如果直接有点数据，那么直接如下读取点就好了
    # pnts = gpd.read_file(r'...')

    run(pnts, recorder)
