"""
   dict 客户端
   发起请求，展示结果
"""

from socket import *
from getpass import getpass

HOST = '127.0.0.1'
PORT = 8888
ADDR = (HOST, PORT)
# 所有函数都用s
s = socket()
s.connect(ADDR)


# 查单词
def do_query(name):
    while True:
        word = input("单词：")
        if word == '##':  # 结束单词查询
            break
        msg = 'Q %s %s' % (name, word)
        s.send(msg.encode())
        # 等待回复
        data = s.recv(2048).decode()
        print(data)


# 查历史记录
def do_history(name):
    msg = 'H %s' % name
    s.send(msg.encode())
    # 等待回复
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                return
            else:
                print(data)
    else:
        print("没有当前用户的历史记录。")




# 二级界面
def login(name):
    while True:
        print("""
        ================Query===============
        1. 查单词      2.历史记录      3.注销
        ====================================
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_history(name)
        elif cmd == '3':
            return
        else:
            print("请输入正确命令！")


# 注册
def do_register():
    while True:
        name = input("User:")
        passwd = getpass()
        passwd1 = getpass("Again:")
        if (' ' in name) or (' ' in passwd):
            print("用户名或密码不能有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = "R %s %s" % (name, passwd)
        # 发送请求
        s.send(msg.encode())
        # 接收反馈
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return


# 登录
def do_login():
    name = input("User:")
    passwd = getpass()
    msg = 'L %s %s' % (name, passwd)
    s.send(msg.encode())
    # 等待反馈
    data = s.recv(128).decode()
    if data == 'OK':
        print("登录成功")
        login(name)
    else:
        print("登录失败")


# 创建网络连接
def main():
    while True:
        print("""
        ===============Welcome==============
        1. 注册         2.登录         3.退出
        ====================================
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            s.send(b'E')
            print("谢谢使用！")
            return
        else:
            print("请输入正确命令！")


if __name__ == "__main__":
    main()
