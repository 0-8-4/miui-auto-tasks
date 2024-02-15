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
from twocaptcha import TwoCaptcha

_conf = ConfigManager.data_obj

def find_key(data: dict, key: str):
    """递归查找字典中的key"""
    for dkey, dvalue in data.items():
        if dkey == key:
            return dvalue
        if isinstance(dvalue, dict):
            find_key(dvalue, key)
    return None

async def get_validate(gt: str, challenge: str, url: str) -> GeetestResult:  # pylint: disable=invalid-name
    """获取人机验证结果"""
    try:
        validate = None
        if _conf.preference.api_key:
            solver = TwoCaptcha(_conf.preference.api_key)
            geetest_data = solver.geetest(gt=gt,
            apiServer='api.geetest.com',
            challenge=challenge,userAgent='Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
            url=url)
            log.info("极验证返回:" + str(geetest_data))
            # 解析 code 字段为字典对象
            code_data = json.loads(geetest_data['code'])
            # 获取 geetest_challenge 和 geetest_validate 的值
            challenge = code_data['geetest_challenge']
            validate = code_data['geetest_validate']
            id = geetest_data['captchaId']
            return GeetestResult(challenge=challenge, validate=validate, captchaId=id)
        else:
            return GeetestResult(challenge="", validate="")
    except Exception:  # pylint: disable=broad-exception-caught
        log.exception("获取人机验证结果异常")
        return GeetestResult(challenge="", validate="")
