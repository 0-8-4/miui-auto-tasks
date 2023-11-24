'''
Date: 2023-11-12 14:05:06
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-24 13:10:39
'''
import os
import sys

from loguru import logger


class InterceptHandler:
    """拦截器"""

    message = ""
    """消息"""

    def __init__(self, record: dict):
        self.write(record)

    def write(self, record: dict):
        """写入"""
        InterceptHandler.message += record.get('message')

path_log = os.path.join("logs", '日志文件.log')
log = logger
log.remove()

log.add(sys.stdout, level="INFO", colorize=True,
        format="<cyan>{module}</cyan>.<cyan>{function}</cyan>"
               ":<cyan>{line}</cyan> - "
               "<level>{message}</level>", filter=InterceptHandler)

log.add(path_log, level="DEBUG",
        format="{time:HH:mm:ss} - "
               "{level}\t| "
               "{module}.{function}:{line} - {message}",
        rotation="1 days", enqueue=True, serialize=False, encoding="utf-8", retention="10 days")
