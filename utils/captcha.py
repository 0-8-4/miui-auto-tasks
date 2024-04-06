'''
Date: 2023-11-13 19:55:22
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-12-18 20:46:51
'''
import json

from .request import post
from .logger import log
from .config import ConfigManager
from .data_model import ApiResultHandler, GeetestResult

_conf = ConfigManager.data_obj

def find_key(data: dict, key: str):
    """递归查找字典中的key"""
    for dkey, dvalue in data.items():
        if dkey == key:
            return dvalue
        if isinstance(dvalue, dict):
            find_key(dvalue, key)
    return None

async def get_validate(gt: str, challenge: str) -> GeetestResult:  # pylint: disable=invalid-name
    """获取人机验证结果"""
    try:
        validate = None
        if _conf.preference.geetest_url:
            params = _conf.preference.geetest_params.copy()
            params = json.loads(json.dumps(params).replace("{gt}", gt).replace("{challenge}", challenge))
            data = _conf.preference.geetest_data.copy()
            data = json.loads(json.dumps(data).replace("{gt}", gt).replace("{challenge}", challenge))
            response = await post(
                _conf.preference.geetest_url,
                params=params,
                json=data,
            )
            log.debug(response.text)
            geetest_data = response.json()
            geetest = ApiResultHandler(geetest_data)
            challenge = find_key(geetest.data, "challenge")
            validate = find_key(geetest.data, "validate")
            return GeetestResult(challenge=challenge, validate=validate)
        else:
            return GeetestResult(challenge="", validate="")
    except Exception:  # pylint: disable=broad-exception-caught
        log.exception("获取人机验证结果异常")
        return GeetestResult(challenge="", validate="")
