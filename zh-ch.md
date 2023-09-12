中文版 [ENGLISH](./README.md)

# SREETVIEW_IMAGES_CRAWLER

## 爬取思路与原理：

![tech](./pics/tech.png)

<p align="center">
        <i>技术路线.</i>
</p>

![prin](./pics/pics.png)

<p align="center">
        <i>实现原理.</i>
</p>

## 使用说明：

### 代码运行顺序：

> 2023.09.13 更新: 仅抓取特定年份街景数据 (如仅抓取 2017 -> 在 config.py 中配置 IMAGE_YEAR = 2017)

- 在 config/config.py 中配置你的个人百度地图 Key(需要到百度地图官网注册账号领取)
- main.py 修改你的数据路径
- 执行 main.py

### 内容：

- 爬取文件的命名规则为 {wgs84*lng}*{wgs84*lat}*{direction}\_{pitch}；其中 direction 指 360° 街景图片的角度，0 为正前方；pitch 为仰角；
- 用户需要手动配置的目录为 config/config.py 及 main.py,其他技术文件一般不需要额外配置
- main.py 中，注意输入数据类型。若输入城市路网数据，则需在 main.py 中调用 points_from_road 函数，用生成的 pnts 调用 run 函数；，若输入街景点精确精确点数据，则直接调用 run 函数即可
- recorder 是最终输出的爬取记录 excel 数据
- dir 文件夹：放置了部分示例数据 如 dir/shp/roads.shp 为示例道路，points 为示例点
- dir 文件夹：爬取进程结束后，crawl_recorder.xlsx 生成，会记录所有坐标点的爬取结果![p](./pics/1683623741567.png)
- images 文件夹：保存街景爬取结果的文件夹

### 环境依赖：

- python 3.8 以上
- 需要有 pandas,geopandas,tqdm 等第三方库

### 注意事项:

- 注意开始爬虫的启动文件必须为 geodataframe 格式下的点数据
- wgs84 坐标在程序中会利用 wgs2bd09mc 函数自动转化为百度的坐标，无需额外操作。
- 街景文件命名方式为：经度 纬度 角度 俯仰角，若爬取成功，每个点会爬取 0 度、90 度、180 度和 270 度的街景图。

### 参考文献：

- Yao, Y., Liang, Z., Yuan, Z., Liu, P., Bie, Y., Zhang, J., ... & Guan, Q. (2019). A human-machine adversarial scoring framework for urban perception assessment using street-view images. International Journal of Geographical Information Science, 33(12), 2363-2384.

## 声明：

本爬虫代码仅供个人学习科研使用，请勿用于任何非科研和非法用途。
欢迎随时技术交流(kingsleyl0107@gmail.com)
