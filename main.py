from requestClass import *
from multiprocessing import *
from protocol_parse import *
from mysqltest import *
from action import *
from maincheck import check


def main():

    # requestPool = requestPool(10000)
    while True:
        request = request_handle(s)
        if request == []:
            print(request)
        else:
            request = requestDeal(request)
            # try:
            #     requestPool.append(request)
            # except:
            #     print("请求太多，装不下了")
            # for request in requestPool:
            #     requestPool.remove(request)
            ip = request.ip
            requestData = request.requestData
            get_ = requestData.get('GET') or requestData.get('POST')
            if 'css' not in get_ or 'js' not in get_ or 'ico' not in get_:
                status, risk = check(request, ip)
                response = request.sendToStart()
                resend(response, status)
                if status == 2:
                    handle(ip, risk)


if __name__ == '__main__':
    # requestPool = requestPool(10000)
    # size = requestPool.size
    s = protocol_parse()
    try:
        main()
    except BaseException as e:
        print(e)
        main()
