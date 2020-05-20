# 定时任务模块
# 具体使用方法参考 https://schedule.readthedocs.io/en/stable/#issues
# github.com/dbader/schedule
import schedule
import time
# 封装的微信的api
from wechat import login, sendMessageToMyself, sendMessageToFriend

login()

def job():
    print("I'm working...")
    # 给微信自己发送一条消息
    sendMessageToMyself("I'm working...")
# 执行一次任务
job()
# 设计定时任务
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)