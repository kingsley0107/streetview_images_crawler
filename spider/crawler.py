import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.config import BMAP_API_KEY
from utils.header import get_header


def wgs2bd09mc(wgs_x, wgs_y):
    base_url = "http://api.map.baidu.com/geoconv/v1/"
    wgs_coord = str(wgs_x) + "," + str(wgs_y)
    # to = 6 : bd09mc status
    params = {"coords": wgs_coord, "from": 1, "to": 6, "ak": BMAP_API_KEY}
    response = request_url(base_url, params)
    if response.status_code == 200:
        bd_coords = response.json()["result"][0]
        bd_x, bd_y = bd_coords["x"], bd_coords["y"]
        return bd_x, bd_y


def getPanoId(bd_x, bd_y):
    base_url = f"https://mapsv0.bdimg.com/"
    params = {"qt": "qsdata", "x": bd_x, "y": bd_y}
    response = request_url(base_url, params)
    content = response.json()
    PanoId = content["content"]["id"]
    return PanoId


def getPanoMeta(PanoId):
    base_url = "https://mapsv0.bdimg.com/"
    params = {"qt": "sdata", "sid": PanoId, "pc": 1}
    response = request_url(base_url, params)
    content = response.json()["content"][0]
    date = content["Date"]
    name = content["Rname"]
    return {"date": date, "name": name}


def getImage(PanoId, direction=0, pitch=0, width=1024, height=1024):
    base_url = "https://mapsv0.bdimg.com/"
    params = {
        "qt": "pr3d",
        "fovy": 90,
        "quality": 100,
        "panoid": PanoId,
        "heading": direction,
        "pitch": pitch,
        "width": width,
        "height": height,
    }
    response = request_url(base_url, params)
    if response.status_code == 200 and response.headers.get("Content-Type"):
        return response


def request_url(url, params=None):
    header = get_header()
    # proxy = {"http": random.choice(proxies_pool), "https": random.choice(proxies_pool)}
    retry_times = 5
    retry_delay = 1
    session = requests.Session()
    retry = Retry(total=retry_times, backoff_factor=retry_delay)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    response = session.get(url, params=params, headers=header)
    return response
