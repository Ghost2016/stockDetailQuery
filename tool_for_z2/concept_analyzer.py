#!/usr/bin/env python
#coding: utf-8

from collections import Counter

def analyze_stock_concepts(stock_data_list):
    """
    分析股票概念分布
    
    Args:
        stock_data_list: 股票数据列表，每个股票数据包含'所属概念'字段
        
    Returns:
        list: 按出现次数排序的概念分布结果，格式：【概念名称 - 出现次数】
    """
    concept_counter = Counter()
    
    # 遍历所有股票数据
    for stock in stock_data_list:
        concepts_str = stock.get('所属概念', '')
        
        if concepts_str:
            # 按分号分割概念并统计
            concepts = [concept.strip() for concept in concepts_str.split('；') if concept.strip()]
            concept_counter.update(concepts)
    
    # 格式化结果并按出现次数排序
    result = []
    for concept, count in concept_counter.most_common():
        result.append("【{} - {}】".format(concept, count))
    
    return result

# 示例用法
if __name__ == '__main__':
    # 示例股票数据
    example_stock_data = [
        {
            '股票代码': '688110.SH',
            '股票简称': '东芯股份',
            '所属概念': '汽车芯片；存储芯片；5G；芯片概念；消费电子概念；安防；专精特新；车联网(车路协同)；回购增持再贷款概念；沪股通；融资融券'
        },
        {
            '股票代码': '000001.SZ',
            '股票简称': '平安银行',
            '所属概念': '芯片概念；安防；融资融券；银行'
        }
    ]
    
    # 分析概念分布
    concept_distribution = analyze_stock_concepts(example_stock_data)
    
    # 打印结果
    print("股票概念分布统计：")
    for i, concept in enumerate(concept_distribution, 1):
        print("{}. {}".format(i, concept)) 