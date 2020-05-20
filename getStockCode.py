import requests
from ghost import Ghost
from requests.cookies import RequestsCookieJar
import re
import json
import types
import sys

def printlist(resultList):
    if type(resultList) is list:
        for i in resultList:
           printlist(i)
    else:
        if type(resultList) is bytes:
            print(resultList.encode('utf-8'))
        else:
            print(resultList)

def dosearch(argname):
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    ghost = Ghost()
    cj = RequestsCookieJar()
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept - Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'Connection': 'Keep-Alive',
               'Host': 'www.iwencai.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36'}

    print(u"同花顺问财选股开始")
    # 获取同花顺为每个股票代码设定的fid
    parms = {'typed': '0', 'f': '1', 'qs': 'result_original', 'tid': 'stockpick', 'ts': '1',
             'w': argname}
    url = 'http://www.iwencai.com/stockpick/search'
    with ghost.start() as session:
        session.delete_cookies()
        session.open(url, method="get", timeout=30)
        session.save_cookies(cj)
    s = requests.Session()
    requestPage = s.get(url, params=parms, headers=headers, timeout=3,cookies=cj)

    match=re.search(r'allResult = {(.+)};',requestPage.text)
    stockinfo=''
    if match :
        stockinfo = str(match.group(1))
    stocklist="{"
    stocklist += stockinfo
    stocklist += "}"
    stockinfo ="{"+stockinfo+"}"
    decodejson = json.loads(stockinfo)
    total = str(decodejson['total'])
    print('总共有:%s个,分别为：' % total)
    wccode2hq = decodejson['wccode2hq']
    for j in wccode2hq:
        print(j)
    title = str(decodejson['title'])
    # print('标题：%s' % title.decode('unicode-escape').encode('utf-8'))
    print('标题：%s' % title)
    result = decodejson['result']
    dataidx=1
    if type(result) is list:
        for i in result:
            print('------第%d行数据打印开始------'%dataidx)
            printlist(i)
            # print('------第%d行数据打印结束--------'%dataidx)
            dataidx+=1


def main():
    # args = '本周板块指数创新高 本周成交量/上周成交量 周阳线 由高到低排序'
    args = '板块指数 本周成交量/上周成交量 由高到低排序 周阳线'
    # 所属概念包含XXX 本周成交量/上周成交量 由高到低 周阳线
    # args = '所属概念包含白马股'
    dosearch(args)


if __name__ == '__main__':
    main()