import random
import requests


def get_proxy():
    response = requests.get(
        "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=b4a9bc5dd82e4dbdafcf70327c894bf9&orderno=YZ2023596057VUtu4h&returnType=1&count=10"
    )
    proxies_pool = response.text.split("\r\n")
    return random.choice(proxies_pool)
