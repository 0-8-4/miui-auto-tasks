"""
Date: 2023-11-13 19:55:22
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-01-24 22:02:00
"""

import json
import time

from jsonpath_ng import parse

from .config import ConfigManager
from .data_model import GeetestResult
from .logger import log
from .request import request

_conf = ConfigManager.data_obj


def find_key(data: dict, key: str):
    """递归查找字典中的key"""
    for dkey, dvalue in data.items():
        if dkey == key:
            return dvalue
        if isinstance(dvalue, dict):
            find_key(dvalue, key)
    return None


def get_validate_other(
    gt: str, challenge: str
) -> GeetestResult:  # pylint: disable=invalid-name
    """获取人机验证结果"""
    try:
        validate = ""
        if _conf.preference.get_geetest_url:
            params = _conf.preference.get_geetest_params.copy()
            params = json.loads(
                json.dumps(params).replace("{gt}", gt).replace("{challenge}", challenge)
            )
            data = _conf.preference.get_geetest_data.copy()
            data = json.loads(
                json.dumps(data).replace("{gt}", gt).replace("{challenge}", challenge)
            )
            for i in range(10):
                log.info(f"第{i}次获取结果")
                response = request(
                    _conf.preference.get_geetest_method,
                    _conf.preference.get_geetest_url,
                    params=params,
                    json=data,
                )
                log.debug(response.text)
                result = response.json()
                geetest_validate_expr = parse(
                    _conf.preference.get_geetest_validate_path
                )
                geetest_validate_match = geetest_validate_expr.find(result)
                if len(geetest_validate_match) > 0:
                    validate = geetest_validate_match[0].value
                geetest_challenge_expr = parse(
                    _conf.preference.get_geetest_challenge_path
                )
                geetest_challenge_match = geetest_challenge_expr.find(result)
                if len(geetest_challenge_match) > 0:
                    challenge = geetest_challenge_match[0].value
                if validate and challenge:
                    return GeetestResult(challenge=challenge, validate=validate)
                time.sleep(1)
            return GeetestResult(challenge="", validate="")
        else:
            return GeetestResult(challenge="", validate="")
    except Exception:  # pylint: disable=broad-exception-caught
        log.exception("获取人机验证结果异常")
        return GeetestResult(challenge="", validate="")


def get_validate(
    gt: str, challenge: str
) -> GeetestResult:  # pylint: disable=invalid-name
    """创建人机验证并结果"""
    try:
        validate = ""
        if _conf.preference.geetest_url:
            params = _conf.preference.geetest_params.copy()
            params = json.loads(
                json.dumps(params).replace("{gt}", gt).replace("{challenge}", challenge)
            )
            data = _conf.preference.geetest_data.copy()
            data = json.loads(
                json.dumps(data).replace("{gt}", gt).replace("{challenge}", challenge)
            )
            response = request(
                _conf.preference.geetest_method,
                _conf.preference.geetest_url,
                params=params,
                json=data,
            )
            log.debug(response.text)
            result = response.json()
            geetest_validate_expr = parse(_conf.preference.geetest_validate_path)
            geetest_validate_match = geetest_validate_expr.find(result)
            if len(geetest_validate_match) > 0:
                validate = geetest_validate_match[0].value
            geetest_challenge_expr = parse(_conf.preference.geetest_challenge_path)
            geetest_challenge_match = geetest_challenge_expr.find(result)
            if len(geetest_challenge_match) > 0:
                challenge = geetest_challenge_match[0].value
            if validate and challenge:
                return GeetestResult(challenge=challenge, validate=validate)
            else:
                return get_validate_other(gt=gt, challenge=challenge)
        else:
            return GeetestResult(challenge="", validate="")
    except Exception:  # pylint: disable=broad-exception-caught
        log.exception("获取人机验证结果异常")
        return GeetestResult(challenge="", validate="")
