#!/usr/bin/env python
#coding: utf-8

from meepwn import crawl_stock_data
from collections import Counter
import json

def analyze_concept_distribution(stock_data_list):
    """
    分析股票数据中所属概念的分布情况
    
    Args:
        stock_data_list: 股票数据列表，每个元素包含股票的各种信息
        
    Returns:
        dict: 概念分布字典，按出现次数从大到小排列
    """
    concept_counter = Counter()
    
    for stock in stock_data_list:
        # 获取所属概念字段
        concepts_str = stock.get('所属概念', '')
        
        if concepts_str:
            # 按分号分割概念
            concepts = [concept.strip() for concept in concepts_str.split('；') if concept.strip()]
            
            # 统计每个概念
            for concept in concepts:
                concept_counter[concept] += 1
    
    return concept_counter

def format_concept_distribution(concept_counter):
    """
    格式化概念分布结果
    
    Args:
        concept_counter: Counter对象，包含概念及其出现次数
        
    Returns:
        list: 格式化后的结果列表
    """
    # 按出现次数从大到小排序
    sorted_concepts = concept_counter.most_common()
    
    formatted_results = []
    for concept, count in sorted_concepts:
        formatted_results.append("【{} - {}】".format(concept, count))
    
    return formatted_results

def get_concept_distribution_from_question(question="今日涨停"):
    """
    根据问财查询条件获取股票数据并分析概念分布
    
    Args:
        question: 问财查询条件
        
    Returns:
        list: 格式化后的概念分布结果
    """
    print("正在查询：{}".format(question))
    
    # 获取股票数据
    stock_data_list = crawl_stock_data(question)
    
    if not stock_data_list:
        print("未获取到股票数据")
        return []
    
    print("获取到 {} 只股票数据".format(len(stock_data_list)))
    
    # 分析概念分布
    concept_counter = analyze_concept_distribution(stock_data_list)
    
    if not concept_counter:
        print("未找到概念数据")
        return []
    
    # 格式化结果
    formatted_results = format_concept_distribution(concept_counter)
    
    return formatted_results, concept_counter

def print_concept_distribution(formatted_results, top_n=None):
    """
    打印概念分布结果
    
    Args:
        formatted_results: 格式化后的结果列表
        top_n: 显示前N个概念，如果为None则显示全部
    """
    if not formatted_results:
        print("没有概念分布数据")
        return
    
    print("\n=== 股票概念分布统计 ===")
    
    display_results = formatted_results[:top_n] if top_n else formatted_results
    
    for i, result in enumerate(display_results, 1):
        print("{:2d}. {}".format(i, result))
    
    if top_n and len(formatted_results) > top_n:
        print("\n... 还有 {} 个概念".format(len(formatted_results) - top_n))
    
    print("\n总共统计了 {} 个不同概念".format(len(formatted_results)))

if __name__ == '__main__':
    # 示例用法
    
    # 可以修改查询条件
    question = "今日涨停"  # 默认查询今日涨停的股票
    
    # 获取概念分布
    formatted_results, concept_counter = get_concept_distribution_from_question(question)
    
    if formatted_results:
        # 打印前20个最热门概念
        print_concept_distribution(formatted_results, top_n=20)
        
        # 也可以打印全部概念
        # print_concept_distribution(formatted_results)
        
        # 如果需要获取具体的统计数据
        print("\n=== 详细统计信息 ===")
        print("概念总数: {}".format(len(concept_counter)))
        total_stocks = sum(concept_counter.values())//len(concept_counter) if concept_counter else 0
        print("股票总数: {}".format(total_stocks))
        
        # 打印前5个最热门概念的详细信息
        print("\n前5个最热门概念:")
        for concept, count in concept_counter.most_common(5):
            percentage = (count / len(formatted_results)) * 100 if formatted_results else 0
            print("  {}: {} 次 (占比 {:.1f}%)".format(concept, count, percentage)) 