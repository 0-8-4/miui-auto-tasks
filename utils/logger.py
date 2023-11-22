"""
Date: 2023-11-12 14:05:06
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-18 14:20:44
"""
import os
import sys

from loguru import logger

MESSAGE = ""


def log_filter(record: dict):
    """loguru过滤器"""
    global MESSAGE  # pylint: disable=global-statement
    if record["level"].no >= 20:
        MESSAGE += f"{record.get('message')}\n"
    return True


def get_message():
    """
    说明:
        返回消息
    返回:
        收集到的消息
    """
    global MESSAGE  # pylint: disable=global-variable-not-assigned
    return MESSAGE


path_log = os.path.join("logs", '日志文件.log')
log = logger
log.remove()

log.add(sys.stdout, level="INFO", colorize=True,
        format="<cyan>{module}</cyan>.<cyan>{function}</cyan>"
               ":<cyan>{line}</cyan> - "
               "<level>{message}</level>", filter=log_filter)

log.add(path_log, level="DEBUG",
        format="{time:HH:mm:ss} - "
               "{level}\t| "
               "{module}.{function}:{line} - {message}",
        rotation="1 days", enqueue=True, serialize=False, encoding="utf-8", retention="10 days")
