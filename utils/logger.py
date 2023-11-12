'''
Date: 2023-11-11 23:39:10
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-12 13:58:56
'''
import os
import sys

from loguru import logger

message = ""

def LogFilter(record):
    global message
    if record["level"].no >= 20:
        message += f"{record.get('message')}\n"
    return True

def get_message():
    """
    说明:
        返回消息
    返回:
        收集到的消息
    """
    global message
    return message

path_log = os.path.join("logs", '日志文件.log')
log = logger
log.remove()

log.add(sys.stdout, level="INFO", colorize=True,
            format="<cyan>{module}</cyan>.<cyan>{function}</cyan>"
                    ":<cyan>{line}</cyan> - "
                    "<level>{message}</level>",filter=LogFilter)

log.add(path_log, level="DEBUG",
            format="{time:HH:mm:ss} - "
                    "{level}\t| "
                    "{module}.{function}:{line} - {message}",
            rotation="1 days", enqueue=True, serialize=False, encoding="utf-8", retention="10 days")
