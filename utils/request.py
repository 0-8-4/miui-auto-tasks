"""
Date: 2023-11-12 14:05:06
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-18 00:32:53
"""
from typing import Any, Dict, Optional

import httpx
from onepush import notify

from .config import ConfigManager
from .logger import log

_conf = ConfigManager.data_obj


async def get(url: str,
              *,
              headers: Optional[Dict[str, str]] = None,
              params: Optional[Dict[str, Any]] = None,
              timeout: Optional[int] = 20,
              **kwargs) -> httpx.Response:
    """
    说明：
        httpx的get请求封装
    参数：
        :param url: url
        :param headers: 请求头
        :param params: params
        :param data: data
        :param json: json
        :param timeout: 超时时间
    """
    async with httpx.AsyncClient() as client:
        return await client.get(url,
                                headers=headers,
                                params=params,
                                timeout=timeout,
                                **kwargs)


async def post(url: str,
               *,
               headers: Optional[Dict[str, str]] = None,
               params: Optional[Dict[str, Any]] = None,
               timeout: Optional[int] = 20,
               **kwargs) -> httpx.Response:
    """
    说明：
        httpx的post请求封装
    参数：
        :param url: url
        :param headers: 请求头
        :param params: params
        :param data: data
        :param json: json
        :param timeout: 超时时间
    """
    async with httpx.AsyncClient() as client:
        return await client.post(url,
                                 headers=headers,
                                 params=params,
                                 timeout=timeout,
                                 **kwargs)


def notify_me(content=""):
    """
    默认推送日志
    """
    notifier = _conf.ONEPUSH.notifier
    params = _conf.ONEPUSH.params
    if not notifier or not params:
        log.error('未配置推送或未正确配置推送')
        return False
    return notify(notifier, content=content, **params)
