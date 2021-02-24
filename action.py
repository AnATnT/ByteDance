import datetime
import pymysql

# 全局变量，不同封禁等级封禁时间
hour = [0, 1, 12, 24, 72, 168]


# handle方法调用，为内部使用函数
def update(cursor, exist, ip, level):
    date = (datetime.datetime.now() + datetime.timedelta(hours=hour[level])).strftime("%Y-%m-%d "
                                                                                      "%H:%M:%S")
    if exist:
        cursor.execute('update blacklist set level=%s, banTime=%s where ip=%s', [
                       level, date, ip])
    else:
        cursor.execute('insert into blacklist values (%s,%s,%s)', [
                       ip, level, date])


# 处理新黑名单记录，返回值：1为已在白名单，-1为level值不合法，0为处理成功
def handle(ip, level):
    if level >= len(hour) or level < 0:
        return -1
    db = pymysql.connect(
        host='47.104.70.37',
        port=3306,
        user='root',
        password='bytedance',
        db='bytedance'
    )

    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute('select * from whitelist where ip = %s', [ip])
        if cursor.fetchone() is not None:
            return 1
        cursor.execute('select * from blacklist where ip = %s', [ip])
        ret = cursor.fetchone()
        if ret is not None:
            if ret['level'] <= level or datetime.datetime.now() > ret['banTime']:
                update(cursor, True, ip, level)
            else:
                update(cursor, True, ip, ret['level'])
        else:
            update(cursor, False, ip, level)
        db.commit()
    except:
        db.rollback()
        return -1
    finally:
        cursor.close()
        db.close()
    return 0


# 是否为黑名单或白名单里的ip，1为黑名单，2为白名单，0为不在黑/白名单
def isBlackOrWhite(ip):
    db = pymysql.connect(
        host='47.104.70.37',
        port=3306,
        user='root',
        password='bytedance',
        db='bytedance'
    )
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute('select * from whitelist where ip = %s', [ip])
        if cursor.fetchone() is not None:
            return 2
        cursor.execute('select * from blacklist where ip = %s', [ip])
        ret = cursor.fetchone()
        if ret is not None:
            if datetime.datetime.now() > ret['banTime']:
                cursor.execute('delete from blacklist where ip = %s', [ip])
                db.commit()
                return 0
            return 1
    except:
        db.rollback()
    finally:
        cursor.close()
        db.close()
    return 0


# 更改规则（提供给后台的接口，修改不同封禁等级的时长），True为修改成功，False为修改失败
def changeHours(array):
    if not isinstance(array, list):
        return False
    for i, val in enumerate(array):
        if val < 0:
            return False
        if i > 0 and val < array[i-1]:
            return False
    global hour
    hour = array
    return True


if __name__ == '__main__':
    changeHours([0, 1, 2, 1])
    print(hour)
