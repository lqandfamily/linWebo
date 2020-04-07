"""
数据访问基础模块
"""
import sys

import os

# 注入Python搜索路径
sys.path.append(os.getcwd())

import pymysql

from db.dao.sql import initSqlList
from security.encrypt import encrypt

db = pymysql.connect("localhost", "root", "xxx", "webo", autocommit=1)


def createTable():
    cursor = db.cursor()
    # hot_spot表结构: id, 排名(rank)，热搜字(affair)，游览数(view)，创建时间，创建id, 用于搜索
    # spider_data:  id，时间， 创建id
    # 用户表：id, 用户名，密码
    for sql in initSqlList:
        cursor.execute(sql)
    # 写入admin用户
    sqlIns = "insert into t_user values (default,%s,%s)"
    result = cursor.execute(sqlIns, ["admin", encrypt("admin")])
    db.commit()

    print("创建表成功！")


if __name__ == '__main__':
    createTable()
