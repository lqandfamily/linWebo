"""
数据模型
"""
import json
import time


# Json序列化
class HostSpotEntityJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        d = {'rank': obj.rank, 'affair': obj.affair, 'view': obj.view}
        return d


class HostSpotEntity:

    def __init__(self, ID, rank, affair, view, crawlDate, dateID):
        self.ID = ID
        self.rank = rank
        self.affair = affair
        self.view = view
        self.crawlDate = crawlDate
        self.dateId = dateID

    def __str__(self):
        return "{0}  {1}  {2}  {3} {4}" \
            .format(self.rank, self.affair, self.view,
                    self.crawlDate, self.dateId)


class SpiderDateEntity:

    def __init__(self, dateID, crawlDate):
        self.dateId = dateID
        self.crawlDate = crawlDate
