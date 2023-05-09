import pandas as pd
import os

# 到https://lbsyun.baidu.com/ 申请key

# 这个是sample
# BMAP_API_KEY = "DtE9DWaBs56Yxg4pZv8fCGwKG31NXY5W"

BMAP_API_KEY = ""

root = "./"
images = "images/"
img_path = os.path.join(root, images)
recorder = pd.DataFrame(
    columns=[
        "PID",
        "wgs_x",
        "wgs_y",
        "name",
        "date",
        "direction",
        "pitch",
        "status",
        "filename",
    ]
)

# 街景方向，0为正前方
# streetview images' direction, 0 representing the north
headings = [str(i) for i in [0, 90, 180, 270]]

# images angles, 0 represents the horizon
pitchs = 0
