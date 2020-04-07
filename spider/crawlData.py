import requests
import time
from lxml import etree

from db.entity.hostSpot import HostSpotEntity


def crawl():
    # 网址
    url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
    # 模拟浏览器
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/73.0.3683.103 Safari/537.36'}
    # 获取html页面
    html = etree.HTML(requests.get(url, headers=header).text)
    # 获取数据
    ranks = html.xpath('//td[@class="td-01 ranktop"]/text()')
    affair = html.xpath('//td[@class="td-02"]/a/text()')
    views = html.xpath('//td[@class="td-02"]/span/text()')
    affair = affair[1:]  # 剔除置顶榜

    # 封装数据
    hotSpotList = []
    t = time.time()
    for i in range(len(affair)):
        entity = HostSpotEntity(0, ranks[i], affair[i], views[i], t, 0)
        hotSpotList.append(entity)
    return hotSpotList


# 测试爬取
if __name__ == "__main__":
    crawl()
