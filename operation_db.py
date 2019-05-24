"""
   dict项目用于处理数据
"""
import pymysql
import hashlib


# 编写功能类 提供给服务端使用
class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 passwd='12345678',
                 database='elec_dict',
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()  # 连接数据库

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        # self.cur.close()
        self.db.close()

    # 处理注册
    def register(self, name, passwd):
        sql = "select * from userdata where username = '%s'" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False

        # 加密处理
        hash = hashlib.md5((name + 'the-salt').encode())
        hash.update(passwd.encode())

        sql = "insert into userdata (username, password) values (%s,%s);"
        try:
            self.cur.execute(sql, [name, hash.hexdigest()])
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    # 处理登录
    def login(self, name, passwd):
        sql = "select * from userdata where username = '%s'" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        # 用户名不存在
        if not r:
            return False
        # 加密处理输入的密码
        hash = hashlib.md5((name + 'the-salt').encode())
        hash.update(passwd.encode())
        if hash.hexdigest() == r[-1]:
            return True
        else:
            return False

    # 插入历史记录
    def insert_history(self, name, word):
        sql = "insert into history (username, word, time) " \
              "values (%s, %s, curtime());"
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
        except Exception:
            self.db.rollback()

    # 单词查询
    def query(self, word):
        sql = "select explanation from worddict where " \
              "word = %s;"
        self.cur.execute(sql, word)
        r = self.cur.fetchone()
        if r:
            return r[0]
        else:
            return

    # 历史记录查询
    def history(self, name):
        sql = "select * from history where " \
              "username = %s order by id desc limit 10;"
        self.cur.execute(sql, name)
        return self.cur.fetchall()
