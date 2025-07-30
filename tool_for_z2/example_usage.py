#!/usr/bin/env python
#coding: utf-8

from concept_analyzer import analyze_stock_concepts

# 示例：如果您已经有了股票数据
def example_with_existing_data():
    """示例：使用已有的股票数据进行概念分析"""
    
    # 模拟您的股票数据
    stock_data = [
        {
            '股票代码': '688110.SH',
            '股票简称': '东芯股份',
            '最新价': '53.97',
            '最新涨跌幅': '17.326086957',
            '所属概念': '汽车芯片；存储芯片；5G；芯片概念；消费电子概念；安防；专精特新；车联网(车路协同)；回购增持再贷款概念；沪股通；融资融券',
        },
        {
            '股票代码': '000001.SZ', 
            '股票简称': '平安银行',
            '所属概念': '银行；融资融券；沪深300；大盘股'
        },
        {
            '股票代码': '000002.SZ',
            '股票简称': '万科A', 
            '所属概念': '房地产；融资融券；沪深300；大盘股；深证100'
        }
    ]
    
    print("=== 股票概念分布分析示例 ===")
    print("股票数量: {}".format(len(stock_data)))
    print()
    
    # 分析概念分布
    concept_distribution = analyze_stock_concepts(stock_data)
    
    # 打印结果
    print("概念分布统计结果：")
    for i, concept in enumerate(concept_distribution, 1):
        print("{}. {}".format(i, concept))

if __name__ == '__main__':
    example_with_existing_data() 