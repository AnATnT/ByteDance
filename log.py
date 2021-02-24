#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import random
import pymysql
from pymysql.converters import escape_string

# 执行sql语句


def database(sql):
    db = pymysql.connect(  # 打开数据库连接
        host='47.104.70.37',
        port=3306,
        user='root',
        password='bytedance',
        db='bytedance',
        charset='utf8'
    )
    cursor = db.cursor()  # 使用cursor()创建一个游标对象cursor
    try:
        # 使用execute()执行SQL语句
        cursor.execute(sql)
    # 向数据库提交
        db.commit()
    except:
        # 发生错误时回滚
        # print('插入日志')
        db.rollback()
    try:
        data = cursor.fetchall()
        # 关闭数据库连接
        return data
    except:
        pass
    db.close()


# 插入一条攻击日志
def attackLog(ip, attackType, attackCommand, time):
    print(attackType, attackCommand)
    attackCommand = escape_string(attackCommand)
    database("ALTER TABLE attackLog AUTO_INCREMENT =1")
    sql = "insert into attackLog(ip, attackType,attackCommand, time) values('%s','%s','%s','%s')"
    database(sql % (ip, attackType, attackCommand, time))
    print('success')


# 查询所有攻击日志
def selectAttackLog():
    results = database("SELECT * From attackLog")
    for row in results:
        id = row[0]
        ip = row[1]
        attackType = row[2]
        attackCommand = row[3]
        time = row[4]
        print("id=%d, ip=%s, attackType=%s,attackCommand=%s, time=%s" %
              (id, ip, attackType, attackCommand, time))


# 插入一条正常日志
def normalLog(ip, time):
    database("ALTER TABLE normalLog AUTO_INCREMENT =1")
    sql = "insert into normalLog(ip, time) values('%s','%s')"
    database(sql % (ip, time))


# 查询所有正常日志
def selectNormalLog():
    results = database("SELECT * From normalLog")
    for row in results:
        id = row[0]
        ip = row[1]
        time = row[2]
        print("id=%d, ip=%s, time=%s" % (id, ip, time))


if __name__ == '__main__':
    # 测试用例
    ip = "1.1.1.%d" % random.randint(0, 255)
    attackType = "Sql Injection"
    attackCommand = "test1"
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 插入日志
    attackLog(ip, attackType, attackCommand, time)
    normalLog(ip, time)

    # 查询日志
    print("攻击日志：")
    selectAttackLog()
    print("正常日志：")
    selectNormalLog()
