# 股票概念分布分析工具

这个文件夹包含用于分析股票所属概念分布的工具。

## 文件说明

### 📁 核心工具文件

1. **`concept_analyzer.py`** - 核心分析器（推荐使用）
   - 包含主要的概念分析函数 `analyze_stock_concepts()`
   - 输入股票数据列表，输出概念分布统计结果
   - 格式：【概念名称 - 出现次数】

2. **`analyze_concept_distribution.py`** - 完整功能版本
   - 包含完整的分析流程
   - 可以直接从问财查询获取数据并分析
   - 包含详细的统计信息和格式化输出

3. **`example_usage.py`** - 使用示例
   - 演示如何使用概念分析器
   - 包含示例数据和调用方法

## 快速使用

### 方法一：直接分析现有数据

```python
from concept_analyzer import analyze_stock_concepts

# 您的股票数据
stock_data = [
    {
        '股票代码': '688110.SH',
        '股票简称': '东芯股份',
        '所属概念': '汽车芯片；存储芯片；5G；芯片概念'
    }
    # ... 更多股票数据
]

# 分析概念分布
results = analyze_stock_concepts(stock_data)

# 打印结果
for concept in results:
    print(concept)  # 输出格式：【概念名称 - 出现次数】
```

### 方法二：从问财查询分析

```python
from analyze_concept_distribution import get_concept_distribution_from_question

# 根据查询条件获取数据并分析
results, counter = get_concept_distribution_from_question("今日涨停")
```

## 输出格式

- 【存储芯片 - 20】
- 【芯片概念 - 8】
- 【安防 - 2】

结果按出现次数从大到小排序。

## 运行测试

在此目录下运行：

```bash
# 测试核心分析器
python concept_analyzer.py

# 测试使用示例
python example_usage.py
``` 