from apscheduler.schedulers.blocking import BlockingScheduler
from miuitask import main
from utils.utils import get_config, w_log

config = get_config()

def timing():
    hour = config.get('hour')
    minute = config.get('minute')
    sched = BlockingScheduler()
    sched.add_job(main, 'cron', hour=hour, minute=minute, id='auto_sign')
    w_log("已开启cron定时模式 每天{}时{}分内执行一次签到任务".format(hour, minute))
    sched.start()

timing()
