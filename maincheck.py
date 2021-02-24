from requestClass import *
from mysqltest import ruleList
from log import *
from action import *
import datetime
import re
import ctypes


def check(request, ip):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    black_or_white = isBlackOrWhite(ip)
    risk = 0
    if black_or_white == 1:
        vulnerable = 'blackListIp'
        attackCommand = 'blackListIp'
        print('黑名单')
        print('插入恶意访问日志')
        # attackLog(ip, vulnerable, attackCommand, now)
        return 0, risk
    if black_or_white == 2:
        print('白名单')
        print("插入正常访问日志")
        # normalLog(ip, now)
        return 1, risk
    requestData = request.requestData
    # 直接获取内存中的数据。
    # get_value = ctypes.cast(address, ctypes.py_object).value
    ruler = ruleList()

    for i in ruler:
        for key, value in requestData.items():
            attackData = re.search(i[2], value)
            if key != 'User-Agent':
                if attackData:
                    vulnerable = i[1]
                    if vulnerable == 'command exec' and key == 'Cookie':
                        pass
                    else:
                        attackCommand = '{}:{}'.format(key, value)
                        risk = i[4]
                        print('插入恶意访问日志')
                        attackLog(ip, vulnerable, attackCommand, now)
                        print(vulnerable, attackCommand)
                        return 2, risk
    else:
        print("插入正常访问日志")
        # normalLog(ip, now)
        return 1, risk
