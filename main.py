import urllib
import requests
import re
import json
import operator

def parseIWencai():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
              'hexin-v':'Ap-UZPK1P49yJzuTtRssgTWgKPgqBPEYDV_3mjHsO86VwLHuOdSD9h0oh-dC'}
    word = urllib.parse.quote('前天没有涨停 昨天涨停后开板 昨天涨幅大于5%')
    url = 'http://www.iwencai.com/stockpick/load-data?typed=1&preParams=&ts=1&f=1&qs=result_rewrite' \
          '&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&queryarea=&w=' + word
    res = requests.get(url,headers=header)
    html = res.text
    jObj = json.loads(html)
    content = ''
    if jObj['success'] == True:
        content = jObj['data']['tableTempl']
    stockList = set(re.findall('(?<=&w=)\d{6}',html,re.S))
    print('Size:',len(stockList))
    for str in stockList:
        print(str)


if __name__ == '__main__':
    parseIWencai()
