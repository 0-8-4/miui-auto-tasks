'''
Date: 2023-11-11 23:49:21
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-12 15:22:48
FilePath: \miui-auto-tasks-master\main.py
'''
import asyncio

from utils.api.login import Login
from utils.api.sign import BaseSign
from utils.config import ConfigManager
from utils.logger import log, get_message
from utils.request import notify_me

_conf = ConfigManager.data_obj

async def main():
    for account in _conf.accounts:
        login_obj = Login(account)
        cookies = await login_obj.login()
        if not cookies:
            continue
        sign_obj = BaseSign(cookies)
        daily_tasks = await sign_obj.check_daily_tasks()
        sign_task_obj = sign_obj.AVAILABLE_SIGNS # 签到任务对象合集
        for task in daily_tasks:
            if not task.showType:
                task_obj = sign_task_obj.get(task.name) # 签到任务对象
                if task_obj:
                    if getattr(account, task_obj.__name__):
                        log.info(f"开始执行{task.name}任务")
                        await task_obj(cookies).sign()
                    else:
                        log.info(f"{task.name}任务已被禁用")
                else:
                    log.error(f"未找到{task.name}任务")
            else:
                log.info(f"{task.name}任务已完成")
    notify_me(get_message())

if __name__ == "__main__":
    asyncio.run(main())
