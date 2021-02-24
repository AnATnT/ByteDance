import socket
import socketserver



def request_handle(s):
    '''
    lx: 监听特定地址，调用处理函数
    :param s:
    '''

    conn, addr = s.accept()  # 接受一个浏览器发来的http请求包
    data = getheaders(conn)
    return data


def getheaders(conn):
    '''
    lx: 处理请求头并加以分割
    :param conn: 接收到的某个连接对应的套接字
    :return: 原始请求内容、解析字典、套接字
    '''
    headers = ''
    while True:
        buf = conn.recv(2048).decode('utf-8')
        headers += buf
        if len(buf) < 2048:
            break

    text = headers.split("\r\n")  # 分割请求头

    length = len(text)
    i = 0
    while i < length and len(text[i]) == 0:
        i += 1
    if i >= length:
        print("无请求内容")
        return []
    headers_dict = {}

    # 分割请求行
    method = text[i].split(' ')[0]  # 请求方法
    # headers_dict[str(method)]=text[i].split(method+" ")[-1] #直接截取最后，如果GET后面的信息还含有GET的话会遗漏
    index = text[i].find(method)+len(method)
    j = index
    while j < len(text[i]) and text[i][j] == ' ':
        j += 1
    headers_dict[str(method)] = text[i][j:]

    i += 1
    while i < length:
        if len(text[i]) == 0 or text[i] == '\r' or text[i] == '\n':  # 空行 回车符或换行符
            i += 1
            break
        index = text[i].find(":")
        aft = index+1
        while aft < len(text[i]) and text[i][aft] == ' ':  # 去除:和其后的值之间的空格
            aft += 1
        headers_dict[text[i][0:index]] = text[i][aft:]
        i += 1
    while i < length and text[i] == "":
        i += 1
    if i < length:
        headers_dict["body"] = ""
        while i < length:
            headers_dict["body"] += text[i]  # 空行后的请求包体
            i += 1
    return (headers, headers_dict, conn)  # 将原始请求内容、解析字典、套接字移交规则解析模块


def resend(response, status):
    '''
    lx:
    接收被放行的连接所对应的原请求内容、套接字，
    将请求内容转发至8000端口，并将返回信息根据套接字返回
    :return:
    '''
    headers, conn = response  # 接收规则解析模块等处理后，确认放行的原请求头、原套接字
    # print(headers, conn)
    if headers == "":
        return

    # print("之前的headers:")
    # print(headers)
    headers = headers.replace('47.104.70.37:80', '47.104.70.37:8000').replace(
        'keep-alive', 'close').replace('gzip', '')  # 修改headers，把目标host改为8000端口；关闭长连接和压缩，方便修改服务器返回的网页
    # print("修改后：")
    # print(headers)

    # 新开一个socket，转发请求至原网页
    # print("转发")
    s1 = socket.socket()
    s1.connect(('47.104.70.37', 8000))
    s1.sendall(headers.encode())

    resp = b''
    # 接收返回信息
    while True:
        try:
            buf = s1.recv(1024 * 8)
        except socket.timeout as e:
            print(e)
            break

        resp += buf
        if not buf or buf.startswith(b'WebSocket') and buf.endswith(b'\r\n\r\n'):
            break

    # print("返回信息修改前:")
    if status != 0 and status != 2:
        resp = resp.replace(b'Content-Encoding: gzip\r\n',
                            b'').replace(b'47.104.70.37:8000', b'47.104.70.37:80')
        # print("修改后：")
        # print(resp)

        # 把网页返回
        # print('send to', addr)
        # print("转发")
        conn.sendall(resp)
        conn.close()
        print('请求未被拦截')
    else:
        conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n <h1>???,hacker!!!</h1>')
        conn.close()
        print('被waf拦截')


def protocol_parse():
    '''
    lx：协议解析模块
    开启监听和请求处理
    :return:
    '''
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 80))  # 监听80端口
    s.listen(1500)
    print("监听已启动……")
    return s


