import os
import time

import xlwt
from db.dao.hostSpot import HostSpotDao, SpiderDataDao

# Dao
hostSpotDao = HostSpotDao()
spiderDataDao = SpiderDataDao()


def createTable(fileName):
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("sheet" + fileName)
    worksheet = workbook.get_sheet("sheet" + fileName)
    # 表头
    worksheet.write(0, 0, "排名")
    worksheet.write(0, 1, "关键字")
    worksheet.write(0, 2, "热搜度")
    worksheet.write(0, 3, "时间")
    return workbook


def writeData(data, filename):
    if not data:
        return False

    # 创建工作簿
    workbook = createTable(filename)
    worksheet = workbook.get_sheet("sheet" + filename)

    # 写入数据
    row = 1
    for it in data:
        worksheet.write(row, 0, it.rank)
        worksheet.write(row, 1, it.affair)
        worksheet.write(row, 2, it.view)
        worksheet.write(row, 3, str(it.crawlDate))
        row += 1
    workbook.save(filename + '.xls')


def saveOne(dateId):
    data = hostSpotDao.selByOneDate(dateId)
    if not data:
        return False
    dateName = str(data[0].crawlDate).replace(" ", "_").replace(":", '-')
    writeData(data, dateName)


# 分多个文件保存
def saveDepartMany(timeIds):
    for x in timeIds:
        saveOne(x)


# 将选择多大多个数据保存到一个文件
def saveSelWholeMany(timeIds):
    ll = hostSpotDao.selByManyTime(timeIds)
    writeData(ll, "selected_all")


def saveAllDepart():
    allTime = spiderDataDao.selAll()
    if allTime is None:
        return False
    timeIds = []
    for t in allTime:
        timeIds.append(t.dateId)
    saveDepartMany(timeIds)


def saveAllWhole():
    allTime = spiderDataDao.selAll()
    if allTime is None:
        return False
    ll = hostSpotDao.selByManyTime(allTime)
    writeData(ll, "all")


if __name__ == "__main__":
    # saveDepartMany([1, 2, 3, 10])
    saveSelWholeMany([1, 2, 3, 10])
    # saveAllDepart()
    # saveAllWhole()
