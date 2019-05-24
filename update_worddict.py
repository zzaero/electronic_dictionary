"""
  将单词表导入到数据库,只运行一次
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

# 更新单词表worddict

f = open('/Users/zz/Desktop/tarena/month02/project/project/dict.txt')

for line in f:
    """
    可使用正则表达式匹配内容元组
    tup = re.findall(r'(\w+)\s+(.*)',line)[0]
    """
    word_end_index = 0
    while line[word_end_index] != " ":
        word_end_index += 1
    exp_start_index = word_end_index
    while line[exp_start_index] == " ":
        exp_start_index += 1
    word = line[:word_end_index]
    explanation = line[exp_start_index:]

    try:
        sql = "insert into worddict (word, explanation) values (%s, %s);"
        cur.execute(sql, [word, explanation])
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        break

f.close()
cur.close()
db.close()
