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
### 内容：
- 用户需要手动配置的目录为config/config.py及main.py,其他技术文件一般不需要额外配置
- dir文件夹：放置了部分示例数据 如dir/shp/roads.shp为示例道路，points为示例点
- dir文件夹：爬取进程结束后，crawl_recorder.xlsx生成，会记录所有坐标点的爬取结果![p](./pics/1683623741567.png)
- images文件夹：保存街景爬取结果的文件夹

### 环境依赖：
- python 3.8以上
- 需要有pandas,geopandas,tqdm等第三方库

### 注意事项:
- 注意开始爬虫的启动文件必须为geodataframe格式下的点数据
- wgs84坐标在程序中会利用wgs2bd09mc函数自动转化为百度的坐标，无需额外操作。
- 街景文件命名方式为：经度 纬度 角度 俯仰角，若爬取成功，每个点会爬取0度、90度、180度和270度的街景图。

### 参考文献：

-  Yao, Y., Liang, Z., Yuan, Z., Liu, P., Bie, Y., Zhang, J., ... & Guan, Q. (2019). A human-machine adversarial scoring framework for urban perception assessment using street-view images. International Journal of Geographical Information Science, 33(12), 2363-2384.

## 声明：
本爬虫代码仅供个人学习科研使用，请勿用于任何非科研和非法用途。
欢迎随时技术交流(kingsleyl0107@gmail.com)