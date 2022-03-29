#!/usr/bin/env python
#coding: utf-8

import tushare as ts

token='cee7373f5534cd6ac10783e468db6710767cf637007930de27ce3a08'
ts.set_token(token)
pro = ts.pro_api()

def getTushareInstance():
    return pro

