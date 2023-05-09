from config.config import img_path, headings, pitchs, recorder
import pandas as pd
import os
import glob
import geopandas as gpd
from tqdm import tqdm
from spider.crawler import *


def save_img(img_binary, direction, pitch, wgs_x, wgs_y):
    with open(img_path + rf"{wgs_x}_{wgs_y}_{direction}_{pitch}.png", "wb") as f:
        f.write(img_binary)


def insert_record(recorder, **kwargs):
    this_record = pd.DataFrame.from_dict([kwargs])
    recorder = pd.concat([recorder, this_record])
    return recorder


def SVI_crawler(points: gpd.GeoDataFrame, recorder: pd.DataFrame):
    # check folder
    if not os.path.isdir(img_path):
        os.makedirs(img_path)
        print(f"Folder {img_path} created successfully.")
    else:
        print(f"Folder {img_path} already exists.")

    # check existed files
    filename_existed = glob.glob1(img_path, "*.png")

    # genetate points' ID
    if "PID" not in points.columns.tolist():
        points["PID"] = points.index

    # start to crawl each point's images in four directions
    for index, row in tqdm(points.iterrows(), total=points.shape[0]):
        wgs_x, wgs_y = row["geometry"].x, row["geometry"].y
        # first, transform wgs84 coords into bd09mc
        try:
            bd09mc_x, bd09mc_y = wgs2bd09mc(wgs_x, wgs_y)
        except Exception as e:
            recorder = insert_record(
                recorder,
                PID=row["PID"],
                wgs_x=row["geometry"].x,
                wgs_y=row["geometry"].y,
                status="failed in getting bd09mc",
            )
            continue
        # find the nearest streetview point from the bd09mc coordinate above
        # and get the panoId (Images unique Id ) from this point
        try:
            PanoId = getPanoId(bd09mc_x, bd09mc_y)
        except Exception as e:
            recorder = insert_record(
                recorder,
                PID=row["PID"],
                wgs_x=row["geometry"].x,
                wgs_y=row["geometry"].y,
                status="failed in getting panoId",
            )
            continue
        # get the images' info like date, road name and so on
        try:
            meta = getPanoMeta(PanoId)
            meta["PID"] = row["PID"]
        except Exception as e:
            recorder = insert_record(
                recorder,
                PID=row["PID"],
                wgs_x=row["geometry"].x,
                wgs_y=row["geometry"].y,
                status="failed in getting pano Info",
            )
            continue
        # crawl images in 4 directions:0,90,180 and 270 , for a round
        for direction in headings:
            if f"{wgs_x}_{wgs_y}_{direction}_{pitchs}.png" in filename_existed:
                print(
                    f"direction {direction} in {wgs_x}_{wgs_y} has already been crawled!"
                )
                recorder = insert_record(
                    recorder,
                    PID=row["PID"],
                    wgs_x=row["geometry"].x,
                    wgs_y=row["geometry"].y,
                    name=meta["name"],
                    date=meta["date"],
                    direction=direction,
                    pitch=pitchs,
                    status="crawled before already",
                    filename=f"{wgs_x}_{wgs_y}_{direction}_{pitchs}.png",
                )
                continue
            # for one certain direction
            img = getImage(PanoId, direction)
            if img:
                img_binary = img.content
                # if sucess, save the img
                save_img(img_binary, direction, pitchs, wgs_x, wgs_y)
                recorder = insert_record(
                    recorder,
                    PID=row["PID"],
                    wgs_x=row["geometry"].x,
                    wgs_y=row["geometry"].y,
                    name=meta["name"],
                    date=meta["date"],
                    direction=direction,
                    pitch=pitchs,
                    status="sucess",
                    filename=f"{wgs_x}_{wgs_y}_{direction}_{pitchs}.png",
                )
            else:
                print(f"failed to crawled lng:{wgs_x} lat:{wgs_y} panoId:{PanoId}")
                recorder = insert_record(
                    recorder,
                    PID=row["PID"],
                    wgs_x=row["geometry"].x,
                    wgs_y=row["geometry"].y,
                    name=meta["name"],
                    date=meta["date"],
                    direction=direction,
                    pitch=pitchs,
                    status="failed",
                    filename=f"{wgs_x}_{wgs_y}_{direction}_{pitchs}.png",
                )
    return recorder
