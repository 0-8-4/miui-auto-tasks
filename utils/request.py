"""
Date: 2023-11-12 14:05:06
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-01-17 22:42:51
"""

from typing import Any, Dict, Optional

import requests
from onepush import notify

from .config import ConfigManager
from .logger import log

_conf = ConfigManager.data_obj


def get(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = 20,
    **kwargs,
):
    """
    说明：
        get请求封装
    参数：
        :param url: url
        :param headers: 请求头
        :param params: params
        :param data: data
        :param json: json
        :param timeout: 超时时间
    """
    return requests.get(url, headers=headers, params=params, timeout=timeout, **kwargs)


def post(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = 20,
    **kwargs,
):
    """
    说明：
        post请求封装
    参数：
        :param url: url
        :param headers: 请求头
        :param params: params
        :param data: data
        :param json: json
        :param timeout: 超时时间
    """
    return requests.post(url, headers=headers, params=params, timeout=timeout, **kwargs)

def request(
    method: str | bytes,
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = 20,
    **kwargs,
):
    """
    说明：
        request请求封装
    参数：
        :param method: 请求方法
        :param url: url
        :param headers: 请求头
        :param params: params
        :param data: data
        :param json: json
        :param timeout: 超时时间
    """
    return requests.request(method, url, headers=headers, params=params, timeout=timeout, **kwargs)

def notify_me(content=""):
    """
    默认推送日志
    """
    notifier = _conf.ONEPUSH.notifier
    params = _conf.ONEPUSH.params
    if not notifier or not params:
        log.error("未配置推送或未正确配置推送")
        return False
    return notify(notifier, content=content, **params)
