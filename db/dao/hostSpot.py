"""
热搜榜数据访问层
"""
from db.dao.baseDao import db
from spider.crawlData import crawl
from db.entity.hostSpot import SpiderDateEntity, HostSpotEntity
import time


class SpiderDataDao:
    __cursor = db.cursor()

    def ins(self, entity):
        inSql = "insert into spider_date values (default, %s);"

        cursor = self.__cursor
        cursor.execute(inSql, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(entity.crawlDate)))
        # 返回date_id
        self.selDateId(entity)

        return True

    def selAll(self):
        selSql = "select * from spider_date"
        self.__cursor.execute(selSql)
        result = self.__cursor.fetchall()
        if result is None:
            return None
        ll = []
        for x in result:
            tmp = SpiderDateEntity(x[0], x[1])
            ll.append(tmp)
        return ll

    def selByPage(self, page, per_page):
        """
        分页查询
        :param page: 当前页数
        :param per_page: 每页的记录数
        :return:
        """
        pageSql = "select * from spider_date LIMIT %s,%s;"
        self.__cursor.execute(pageSql, [(page - 1) * per_page, per_page])
        result = self.__cursor.fetchall()
        if result is None:
            return None
        ll = []
        for x in result:
            tmp = SpiderDateEntity(x[0], x[1])
            ll.append(tmp)
        return ll

    def selCount(self):
        """
        查询总的记录数
        :return:
        """
        countSql = "select count(*) from spider_date;"
        self.__cursor.execute(countSql)
        result = self.__cursor.fetchone()
        return result[0]

    def selDateId(self, entity):
        selSql = "select date_id from spider_date where crawl_date = %s;"
        self.__cursor.execute(selSql, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(entity.crawlDate)))
        result = self.__cursor.fetchone()
        if result is None:
            return False
        entity.dateId = result[0]
        return True

    def selCrawlTime(self, timeId):
        selSql = "select crawl_date from spider_date where date_id = %s;"
        self.__cursor.execute(selSql, timeId)
        result = self.__cursor.fetchone()
        if result is None:
            return None
        return str(result[0])

    def delete(self, dateId):
        delSql = "delete from spider_date where date_id = %s;"
        self.__cursor.execute(delSql, dateId)
        db.commit()
        return True


class HostSpotDao:
    __cursor = db.cursor()
    __spiderDateDao = SpiderDataDao()

    def insList(self, entities):
        """
        插入一次爬取的数据
        """
        insSql = "insert into hot_spot values (default,%s,%s,%s,%s,%s);"
        # 插入并获取date_id
        spiderDateEntity = SpiderDateEntity(0, entities[0].crawlDate)
        self.__spiderDateDao.ins(spiderDateEntity)
        for item in entities:
            self.__cursor.execute(insSql,
                                  [item.rank, item.affair, item.view,
                                   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.crawlDate)),
                                   spiderDateEntity.dateId])
        db.commit()
        return True

    def selAll(self):
        allTime = self.__spiderDateDao.selAll()
        if allTime is None:
            return None
        timeIds = []
        for t in allTime:
            timeIds.append(t.dateId)
        return self.selByManyTime(timeIds)

    def selByOneDate(self, dateId):
        selSql = "select * from hot_spot where date_id = %s;"
        self.__cursor.execute(selSql, dateId)
        result = self.__cursor.fetchall()
        if result is None:
            return False
        ll = []
        for item in result:
            entity = HostSpotEntity(item[0], item[1], item[2], item[3], item[4], item[5])
            ll.append(entity)
        return ll

    def selByManyTime(self, timeIds):
        ll = []
        if timeIds is None:
            return None
        for x in timeIds:
            ll.extend(self.selByOneDate(x))
        return ll

    def delByOneDate(self, dateId):
        delSql = "delete from hot_spot where date_id = %s;"
        self.__cursor.execute(delSql, dateId)
        self.__spiderDateDao.delete(dateId)
        db.commit()
        return True


def testAdd():
    ll = crawl()
    dao = HostSpotDao()
    dao.insList(ll)


def testDateAdd():
    ll = crawl()
    dao = SpiderDataDao()
    e = SpiderDateEntity(0, ll[0].crawlDate)
    dao.ins(e)
    print(e.dateId)


def testDateSelAll():
    dao = SpiderDataDao()
    for x in dao.selAll():
        print(x)


def testDateSel():
    spiderDate = SpiderDateEntity(0, 1585132334)
    dao = SpiderDataDao()
    dao.selDateId(spiderDate)
    print(spiderDate.dateId)


def testDateDel():
    spiderDate = SpiderDateEntity(3, 1585132334)
    dao = SpiderDataDao()
    dao.delete(spiderDate)


def testSelByOneDate():
    spEntity = SpiderDateEntity(1, 0)
    dao = HostSpotDao()
    ll = dao.selByOneDate(spEntity)
    for item in ll:
        print(item)


def testSelByManyDate():
    dao = HostSpotDao()
    ll = dao.selByManyTime([1, 2])
    for item in ll:
        print(item)


def testDel():
    dao = HostSpotDao()
    dao.delByOneDate(1)


def testSelCrawlDate():
    dao = SpiderDataDao()
    print(dao.selCrawlTime(1))


if __name__ == "__main__":
    # testAdd()
    # testDateAdd()
    # testDateSel()
    # testDateSelAll()
    testSelCrawlDate()
    # testDateDel()
    # testSelByOneDate()
    # testSelByManyDate()
    # testDel()
