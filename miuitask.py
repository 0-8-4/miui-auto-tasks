"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-02-21 22:50:45
LastEditTime: 2024-04-05 22:43:45
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

# new Env("MIUI-Auto-Task") # pylint: disable=missing-module-docstring
# cron 30 8 * * * miuitask.py

import asyncio

from tenacity import Retrying, stop_after_attempt

from utils.api.login import Login
from utils.api.sign import BaseSign, CheckIn
from utils.config import ConfigManager
from utils.logger import InterceptHandler, log
from utils.request import notify_me
from utils.system_info import print_info
from utils.utils import get_token

_conf = ConfigManager.data_obj


async def main():
    """启动签到"""
    print_info()
    for account in _conf.accounts:
        try:
            for attempt in Retrying(stop=stop_after_attempt(2)):
                with attempt:
                    login_obj = Login(account)
                    if cookies := await login_obj.login():
                        await login_obj.checkin_info()
                        sign_obj = BaseSign(account)
                        daily_tasks = await sign_obj.check_daily_tasks()
                        sign_task_obj = sign_obj.AVAILABLE_SIGNS  # 签到任务对象合集
                        for task in daily_tasks:
                            log.info(f"开始执行{task.name}任务")
                            if task.showType:
                                log.info(f"{task.name}任务已完成")
                                continue
                            if not (
                                task_obj := sign_task_obj.get(task.name)
                            ):  # 签到任务对象
                                log.error(f"未找到{task.name}任务")
                                continue
                            if not getattr(account, task_obj.__name__):
                                log.info(f"任务{task.name}被禁用")
                                continue
                            token = (
                                await get_token(cookies["cUserId"])
                                if task_obj == CheckIn
                                else None
                            )
                            status, reason = await task_obj(account, token).sign()
                            if not status and reason == "cookie":
                                raise ValueError("Cookie失效")
                        user_info = await sign_obj.user_info()
                        log.info(f"{user_info.title} 成长值: {user_info.point}")
        except ValueError:
            ...
    notify_me(InterceptHandler.message)


if __name__ == "__main__":
    asyncio.run(main())
