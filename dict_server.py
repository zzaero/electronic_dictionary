"""
  dict 服务端部分
  处理请求逻辑
"""

from multiprocessing import Process
from socket import *
import sys, signal
from operation_db import *
from time import sleep

# 全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)


# 处理注册
def do_register(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]

    if db.register(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')


# 处理登录
def do_login(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]

    if db.login(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')


# 处理查询
def do_query(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]

    # 插入历史记录
    db.insert_history(name, word)
    # 查单词 没查到返回None
    explanation = db.query(word)
    if not explanation:
        c.send("没有找到该单词".encode())
    else:
        msg = "%s : %s" % (word, explanation)
        c.send(msg.encode())


# 处理历史记录查询
def do_history(c, db, data):
    tmp = data.split(' ')
    name = tmp[-1]
    record = db.history(name)
    if not record:
        c.send(b'FAIL')
        return
    c.send(b'OK')
    for item in record:
        msg = "用户名: %s, 单词: %s, 时间: %s" % (item[1], item[2], item[3])
        sleep(0.1)
        c.send(msg.encode())
    sleep(0.1)
    c.send(b'##')


# 处理客户端请求
def do_request(c, db):
    db.create_cursor()  # 生成游标 db.cur
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), ':', data)
        if not data or data[0] == 'E':
            c.close()
            sys.exit("客户端退出。")
        elif data[0] == 'R':
            do_register(c, db, data)
        elif data[0] == 'L':
            do_login(c, db, data)
        elif data[0] == 'Q':
            do_query(c, db, data)
        elif data[0] == 'H':
            do_history(c, db, data)


# 网络连接
def main():
    # 创建数据库连接对象
    db = Database()

    # 创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 等待客户端连接
    print("Listening to port %d..." % PORT)
    while True:
        try:
            c, addr = s.accept()
            print("Connected from", addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        p = Process(target=do_request, args=(c, db))
        p.daemon = True
        p.start()


if __name__ == "__main__":
    main()
