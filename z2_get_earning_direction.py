#!/usr/bin/env python
#coding: utf-8

from meepwn import crawl_stock_data
from collections import Counter

# 无投资意义的概念过滤列表
MEANINGLESS_CONCEPTS = {
    '融资融券', '沪股通', '深股通', '沪深300', '沪深股通', '深证100', 
    '创业板', '主板', '中小板', '北交所', '科创板',
    '证金持股', '外资持股', '机构重仓', '基金重仓',
    '上证50', '中证500', '创业板50', '科创50',
    '国企改革', '央企国企改革', '地方国企改革',
    '股权转让(并购重组)', '分拆上市意愿', '回购增持再贷款概念',
    '同花顺新质50', '同花顺出海50', '同花顺果指数', '同花顺漂亮100', '同花顺中特估100',
    '高股息精选', '中国AI 50', '高端装备',
    '2025中报预增', '2025一季报预增', '参股银行', '互联网保险'
}

# 概念分析功能
def analyze_stock_concepts(stock_data_list, filter_meaningless=False):
    """
    分析股票概念分布
    
    Args:
        stock_data_list: 股票数据列表，每个股票数据包含'所属概念'字段
        filter_meaningless: 是否过滤无投资意义的概念
        
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
            
            # 如果需要过滤，则排除无意义概念
            if filter_meaningless:
                concepts = [c for c in concepts if c not in MEANINGLESS_CONCEPTS]
            
            concept_counter.update(concepts)
    
    # 格式化结果并按出现次数排序
    result = []
    for concept, count in concept_counter.most_common():
        result.append("【{} - {}】".format(concept, count))
    
    return result

# 获取过滤后的概念统计
def get_filtered_concept_stats(stock_data_list):
    """
    获取过滤前后的概念统计对比
    
    Returns:
        tuple: (原始统计, 过滤后统计, Counter对象, 过滤后Counter对象)
    """
    # 原始统计
    original_results = analyze_stock_concepts(stock_data_list, filter_meaningless=False)
    original_counter = Counter()
    
    # 过滤后统计  
    filtered_results = analyze_stock_concepts(stock_data_list, filter_meaningless=True)
    filtered_counter = Counter()
    
    # 构建Counter对象用于详细分析
    for stock in stock_data_list:
        concepts_str = stock.get('所属概念', '')
        if concepts_str:
            concepts = [concept.strip() for concept in concepts_str.split('；') if concept.strip()]
            original_counter.update(concepts)
            
            filtered_concepts = [c for c in concepts if c not in MEANINGLESS_CONCEPTS]
            filtered_counter.update(filtered_concepts)
    
    return original_results, filtered_results, original_counter, filtered_counter

# 获取个股股价创12年以来新高
def get_stock_price_new_high():
  stock_data = crawl_stock_data('个股股价创12年以来年来新高,所属概念板块')
  print("=== 获取到的股票数据 ===")
  print("股票数量: {}".format(len(stock_data)))
  
  # 显示前几个股票的详细信息
  for i, stock in enumerate(stock_data[:3]):
    print("\n股票 {}: {}({})".format(i+1, stock.get('股票简称', ''), stock.get('股票代码', '')))
    print("所属概念: {}".format(stock.get('所属概念', '')))
  
  if len(stock_data) > 3:
    print("\n... 还有 {} 只股票".format(len(stock_data) - 3))
  
  return stock_data

# 分析概念分布
def analyze_new_high_stock_concepts():
  print("=== 分析股价创新高股票的概念分布 ===\n")
  
  # 获取股票数据
  stock_data = get_stock_price_new_high()
  
  if not stock_data:
    print("未获取到股票数据")
    return
  
  # 获取过滤前后的统计数据
  original_results, filtered_results, original_counter, filtered_counter = get_filtered_concept_stats(stock_data)
  
  print("\n" + "="*60)
  print("=== 原始概念分布统计（包含所有概念）===")
  print("="*60)
  print("概念分布统计结果（按出现次数排序）：")
  for i, concept in enumerate(original_results[:15], 1):  # 只显示前15个
    print("{}. {}".format(i, concept))
  
  if len(original_results) > 15:
    print("... 还有 {} 个概念".format(len(original_results) - 15))
  
  print("\n原始统计总共 {} 个不同概念".format(len(original_results)))
  
  print("\n" + "="*60)
  print("=== 过滤后概念分布统计（排除无投资意义概念）===")
  print("="*60)
  
  print("已过滤的概念类型：交易性概念（融资融券、沪深股通等）、指数概念、财报预期等")
  print("\n有投资价值的概念分布（按出现次数排序）：")
  
  for i, concept in enumerate(filtered_results[:20], 1):  # 显示前20个
    print("{}. {}".format(i, concept))
  
  if len(filtered_results) > 20:
    print("... 还有 {} 个概念".format(len(filtered_results) - 20))
  
  print("\n过滤后统计总共 {} 个有投资价值的概念".format(len(filtered_results)))
  print("过滤掉了 {} 个无投资意义的概念".format(len(original_results) - len(filtered_results)))
  
  # 打印前10个最有投资价值的概念详细统计
  if len(filtered_results) > 0:
    print("\n" + "="*60)
    print("=== 前10个最有投资价值的概念详细统计 ===")
    print("="*60)
    
    for i, (concept, count) in enumerate(filtered_counter.most_common(10), 1):
      percentage = (count / len(stock_data)) * 100 if stock_data else 0
      print("{} - {}({:.2f}% 股票)".format(concept, count, percentage))

if __name__ == "__main__":
  analyze_new_high_stock_concepts()