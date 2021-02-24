class data():
    def __init__(self, default=0):
        self.__data = default

    def __get__(self, instance, owner):
        return self.__data


class requestPool(list):
    def __init__(self, poolSize):
        self.__requestList = []
        self.poolSize = poolSize

    # 将request加入request池
    def appendRequest(self, request):
        self.__requestList.append(request)

    # 将request踢出request池

    def deleteRequest(self, request):
        self.__requestList.remove(request)

    @property
    def requestList(self):
        return self.__requestList

    @property
    def size(self):
        return self.poolSize

    # 保证request池不会溢出，溢出数据包xxx，避免压力太大
    @requestList.setter
    def requestList(self):
        if len(self.__requestList) > 10000:
            raise BaseException


class requestDeal():

    originalRequest = data(0)
    requestData = data(0)
    requestSocket = data(0)

    def __init__(self, request):
        self.request = request
        self.originalRequest = self.request[0]
        self.requestData = self.request[1]
        self.requestSocket = self.request[2]

    # 单独抽取ip出来，方便后续模块调用
    @property
    def ip(self):
        ip = self.requestSocket.getpeername()[0]
        return ip

    # 三种状态，0：白名单 or 规则都不匹配；1：黑名单；2：不是黑名单，但规则匹配。

    def sendToLog(self, ip, attackReason, attacktype, status):
        if status == 2:
            # 如果是应用层的规则匹配，日志需记录攻击语句，存入非正常日志
            return (ip, attackReason, attacktype, status)
        # 根据status，将请求存入正常日志
        return (ip, status)

    # risk，根据risk进行操作。
    def sendToAction(self):
        return (ip, risk)

    # 对于没有问题的请求放行。
    def sendToStart(self):
        return (self.originalRequest, self.requestSocket)
