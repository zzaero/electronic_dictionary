"""
   创建表格,只运行一次
   1. 用户资料(ID, username, password)
   2. 查词记录(username, word, time)
   3. 单词表(ID, word, explanation)
"""
import pymysql

# 连接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='12345678',
                     database='elec_dict',
                     charset='utf8')

# 获取游标
cur = db.cursor()

# 创建表格1: 用户资料

try:
    sql = "create table userdata (id int primary key auto_increment," \
          "username varchar(32) not null, password varchar(128) " \
          "not null);"
    cur.execute(sql)
    db.commit()
except Exception as e:
    db.rollback()
    print(e)

# 创建表格2: 查词记录

try:
    sql = "create table history (id int primary key auto_increment," \
          "username varchar(32) not null, word varchar(32) " \
          "not null, time datetime);"
    cur.execute(sql)
    db.commit()
except Exception as e:
    db.rollback()
    print(e)

# 创建表格3: 单词表

try:
    sql = "create table worddict (id int primary key auto_increment," \
          "word varchar(32) not null, explanation text not null);"
    cur.execute(sql)
    db.commit()
except Exception as e:
    db.rollback()
    print(e)

cur.close()
db.close()