# new Env("MIUI-Auto-Task") # pylint: disable=missing-module-docstring
# cron 30 8 * * * miuitask.py

import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.api.login import Login
from utils.api.sign import BaseSign
from utils.config import ConfigManager
from utils.logger import get_message, log
from utils.request import notify_me
from utils.system_info import print_info
from utils.utils import get_token

_conf = ConfigManager.data_obj

async def main():
    """启动签到"""
    print_info()
    for account in _conf.accounts:
        login_obj = Login(account)
        if (cookies := await login_obj.login()):
            token = await get_token(cookies["cUserId"])
            sign_obj = BaseSign(cookies)
            daily_tasks = await sign_obj.check_daily_tasks()
            sign_task_obj = sign_obj.AVAILABLE_SIGNS  # 签到任务对象合集
            for task in daily_tasks:
                if not task.showType:
                    log.info(f"开始执行{task.name}任务")
                    if task_obj := sign_task_obj.get(task.name):  # 签到任务对象
                        if getattr(account, task_obj.__name__):
                            await task_obj(cookies, token).sign()
                        else:
                            log.info(f"任务{task.name}被禁用")
                    else:
                        log.error(f"未找到{task.name}任务")
                else:
                    log.info(f"{task.name}任务已完成")
    notify_me(get_message())


if __name__ == "__main__":
    if _conf.preference.hour and _conf.preference.minute:
        # 创建一个新的事件循环
        loop = asyncio.get_event_loop()
        scheduler = AsyncIOScheduler()
        scheduler.add_job(main, 'cron', hour=_conf.preference.hour, minute=_conf.preference.minute, id='miuitask')
        scheduler.start()
        try:
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            scheduler.shutdown()
    else:
        asyncio.run(main())
        