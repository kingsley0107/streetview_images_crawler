from config.config import GOOGLE_MAPS_API_KEY
import pandas as pd
from spider.header import get_header
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from PIL import Image
import numpy as np
import cv2
from config.config import FEATURE_YEAR
import os


class GSV_recorder:
    def __init__(self) -> None:
        self.recorder = pd.DataFrame()

    def add_gsv_record(self, new_record):
        pass

    @staticmethod
    def gen_record():
        pass


class GSV_Crawler:
    def __init__(self) -> None:
        self.PANO_API = r"https://maps.googleapis.com/maps/api/streetview/metadata"
        self.GSV_API = r"https://maps.googleapis.com/maps/api/streetview"
        self.SIZE = "600x300"
        self.KEY = GOOGLE_MAPS_API_KEY
        self.IMG_PATH = rf"./{FEATURE_YEAR}_GSV/"
        self.check_folder()

    def check_folder(self):
        if not os.path.isdir(self.IMG_PATH):
            os.makedirs(self.IMG_PATH)
            print(f"Folder {self.IMG_PATH} created successfully.")
        else:
            print(f"Folder {self.IMG_PATH} already exists.")

    def save_img(self, img_binary, point_index):
        with open(file=rf"./{FEATURE_YEAR}_GSV/Point_{point_index}.png",
                  mode="wb") as f:
            f.write(img_binary)
        return

    @staticmethod
    def request_url(url, params=None):
        header = get_header()
        retry_times = 5
        retry_delay = 1
        session = requests.Session()
        retry = Retry(total=retry_times, backoff_factor=retry_delay)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get(url, params=params, headers=header)
        return response

    def get_panoid(self, point_geometry):
        lon = point_geometry.x
        lat = point_geometry.y
        params = {
            "size": self.SIZE,
            "location": f"{lat},{lon}",
            "key": self.KEY
        }
        response = self.request_url(self.PANO_API, params).json()
        if response['status'] != 'OK':
            return 0
        pano_id = response['pano_id']
        return pano_id

    def get_SVI(self, pano_id):

        panorama = []
        for heading in [0, 90, 180, 270]:
            params = {
                "size": self.SIZE,
                "pano": pano_id,
                "key": self.KEY,
                "fov": 90,
                "heading": heading,
                "pitch": 0
            }
            img_binary = self.request_url(self.GSV_API, params).content
            # self.save_img(img_binary, 1, heading)
            panorama.append(
                cv2.imdecode(np.frombuffer(img_binary, np.uint8),
                             cv2.IMREAD_COLOR))
            try:
                panorama = Image.fromarray(np.concatenate(panorama, axis=1))
                panorama.save(rf"./{self.IMG_PATH}/{pano_id}.jpg")
            except Exception:
                print("error")
                return 0
            return pano_id


if __name__ == "__main__":
    # Crawler = GSV_Crawler()
    # accident = pd.read_csv(r'./2022_accident.csv')[['Easting',
    #                                                 'Northing']].head(10)
    # accident['geometry'] = gpd.points_from_xy(
    #     accident["Easting"], accident["Northing"],
    #     crs="epsg:27700").to_crs("epsg:4326")
    # accident['GSV_ID'] = accident['geometry'].apply(
    #     lambda x: Crawler.get_SVI(Crawler.get_panoid(x)))
    # accident.to_csv(rf"./{FEATURE_YEAR}_GSV/recorder.csv")
    pass
