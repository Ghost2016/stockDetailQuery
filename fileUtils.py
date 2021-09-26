#!/usr/bin/env python
#coding: utf-8

# 存储用的文件的名字
fileName="totalStockList.txt"

# 保存股票的set
def saveStocks(stocksSet):
    print('saveStock')
    global fileName
    totalWithLF = set()
    # 遍历传进来的票的Set
    for t in stocksSet:
        # 带有换行的全部票添加换行
        totalWithLF.add(t+'\n')
    with open(fileName, 'w') as f:
        if f:
            f.writelines(set(totalWithLF))
            return True
        else:
            return set()

# 获取股票的set
def getStocks():
    print('getStock')
    with open(fileName, 'r') as f:
        if f:
            _temp = f.readlines()
            total = set()
            for t in _temp:
                # 把所有的换行符号全部给替换掉
                total.add(t.replace('\n', ''))
            return total
        else:
            return set()

# 清空股票列表的set
def clearStocks():
    print('clearStock')
    with open(fileName, 'w') as f:
        if f:
            f.truncate()
            return set()
        else:
            return set()

if __name__ == '__main__':
    clearStocks()