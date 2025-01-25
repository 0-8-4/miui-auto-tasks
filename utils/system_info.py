"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-08-20 22:17:31
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-01-19 16:48:47
"""

import platform
from urllib.request import getproxies

from utils.__version__ import VERSION
from utils.logger import log


def print_info():
    """打印系统信息"""
    log.info(f"MIUI-AUTO-TASK {VERSION}")
    log.info("---------- 系统信息 -------------")
    system_info()
    log.info("---------- 项目信息 -------------")
    log.info("这是一个免费且开源的项目，如果你是付费购买获得请务必退款")
    log.info("项目地址：https://github.com/0-8-4/miui-auto-tasks")
    log.info("欢迎 star，感谢所有项目贡献者，已经提交issues的人，帮助项目发展的人")
    log.info("---------- 脚本日志 -------------")


def system_info():
    """系统信息"""
    log.info(show_info("操作系统平台", platform.platform()))
    log.info(show_info("操作系统版本", platform.version()))
    log.info(show_info("操作系统名称", platform.system()))
    log.info(show_info("操作系统位元", platform.architecture()))
    log.info(show_info("操作系统类型", platform.machine()))
    log.info(show_info("处理器信息", platform.processor()))
    log.info(
        show_info(
            "Python 版本",
            str(platform.python_version()) + " " + str(platform.python_build()),
        )
    )
    if getproxies():
        log.info(show_info("系统代理", getproxies()))


def show_info(tip: str, info: str):
    """格式化输出"""
    return f"{tip}: {info}"
