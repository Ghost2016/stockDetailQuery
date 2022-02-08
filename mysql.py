#!/usr/bin/env python3
import pymysql
# from meepwn import partOne

from sentiment import properties,Sentiment
import datetime


def open():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root",
                         password="hope1234", database="ghosts_database")
    return db


def init():
    db = open()
    cursor = db.cursor()

    # 查询所有数据，返回结果默认以元组形式，所以可以进行迭代处理
    for i in cursor.fetchall():
        print(i)
    print('共查询到：', cursor.rowcount, '条数据。')

    # 获取第一行数据
    result_1 = cursor.fetchone()
    print(result_1)

    # 获取前n行数据
    result_3 = cursor.fetchmany(1)
    print(result_3)
    cursor.close
    db.close()


def select(date=str(datetime.datetime.now().date())):
    db = open()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM sentiment WHERE cur_date = \'%s\'' % date)
    # 获取第一行数据
    result_1 = cursor.fetchone()
    print(result_1)
    result={}
    for index in range(len(properties)):
        result[properties[index]]=result_1[index]
    cursor.close()
    db.close()
    return result

def selectOneBefore(id):
    db = open()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM sentiment WHERE id IN (SELECT MAX(id) FROM sentiment WHERE id < %s)' % id)
    # 获取第一行数据
    result_1 = cursor.fetchone()
    result={}
    for index in range(len(properties)):
        result[properties[index]]=result_1[index]
    cursor.close()
    db.close()
    return result


def insert(obj: Sentiment):
    # obj=select()
    db = open()
    cursor = db.cursor()
    sql='INSERT INTO sentiment(cur_date,up_5,down_5,up_num,down_num,up_all,down_all,up_10_2,up_highest) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    arr=[]
    for pro in properties:
        if not pro == 'id':
            arr.append(str(obj[pro]))
    print(arr)
    try:
      # 执行sql语句
      cursor.execute(sql,arr)
      # 提交到数据库执行
      db.commit()
    except Exception as e:
      print('error:', e)
      # Rollback in case there is any error
      db.rollback()
    cursor.close()
    db.close()
    return True

# 涨幅大于0：2470(2473)		跌幅大于0：1950(1947)

# 10cm：
# 涨幅大于5：111(191)	跌幅大于5：26(11)	
# 涨停数量：48(83)		跌停数量：1(0)
# 二连板：11(4)			最高板：7(6)

if __name__ == '__main__':
    # partOne()
    # print(datetime.datetime(2022, 1, 14).date())
    today=select(datetime.datetime.now().date())
    # today=select(datetime.datetime(2022, 1, 14).date())
    lastday=selectOneBefore(today['id'])
    print(today)
    text = '涨幅大于0:%s(%s)            跌幅大于0:%s(%s)\n' % (today['up_all'], lastday['up_all'], today['down_all'], lastday['down_all'])\
            + '\n'\
            +'10cm：\n'\
            +'涨幅大于5:%s(%s)          跌幅大于5:%s(%s)\n' % (today['up_5'], lastday['up_5'], today['down_5'], lastday['down_5'])\
            +'涨停数量:%s(%s)           跌停数量:%s(%s)\n' % (today['up_num'], lastday['up_num'], today['down_num'], lastday['down_num'])\
            +'二连板:%s(%s)             最高板:%s(%s)\n' % (today['up_10_2'], lastday['up_10_2'], today['up_highest'], lastday['up_highest'])
    print(text)
