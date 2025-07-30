# 检查是否是有效节点

from meepwn import crawl_length
# from tushareUtils import getCurrentTradeDay

# currentDay = getCurrentTradeDay()
# currentDay = '20250721'

# 下午涨停个数 / 上午涨停个数 >  1 / 2
def check_length_rate_is_less_than_2():
  length_morning = crawl_length(currentDay + '上午的涨停')
  length_final = crawl_length(currentDay + '下午的涨停')
  afternoon_rise = length_final - length_morning
  morning_rise = length_morning
  print(currentDay, '上午的涨停个数:', morning_rise, '下午的涨停个数:', afternoon_rise)
  rate = round(afternoon_rise / morning_rise, 3)
  print(currentDay,  '涨停个数比例:', rate, '\t——\t', '满足' if rate > 0.5 else '不满足')
  return rate > 0.5

# 上涨家数超过3000
def check_rise_count_is_more_than_3000():
  rise_count = crawl_length(currentDay + '涨跌幅大于0')
  result = rise_count > 3000
  print(currentDay, '上涨家数:',  rise_count, '\t——\t', '满足' if result else '不满足')
  return result

if __name__ == "__main__":
  c1 = check_length_rate_is_less_than_2()
  c2 = check_rise_count_is_more_than_3000()
  if c1 and c2:
    print(currentDay, '结论：\t\t\t\t 是有效节点')
  else:
    print(currentDay, '结论：\t\t\t\t 不是有效节点')







