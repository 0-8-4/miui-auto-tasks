'''
Date: 2023-11-13 19:55:22
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-14 21:30:31
'''

from .request import get, post
from .logger import log
from .config import ConfigManager
from .data_model import ApiResultHandler, GeetestResult

_conf = ConfigManager.data_obj

async def get_validate(gt: str, challenge: str) -> GeetestResult:
    try:
        validate = ""
        if not _conf.preference.geetest_url:
            return GeetestResult(challenge="", validate="")
        params = _conf.preference.geetest_params
        for key, value in params.items():
            if isinstance(value, str):
                params[key] = value.format(gt=gt, challenge=challenge)
        data = _conf.preference.geetest_data
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.format(gt=gt, challenge=challenge)
        response = await post(
            _conf.preference.geetest_url,
            params=params,
            json=data,
        )
        log.debug(response.text)
        geetest_data = response.json()
        geetest = ApiResultHandler(geetest_data)
        challenge = geetest.data["challenge"]
        validate = geetest.data["validate"]
        return GeetestResult(challenge=challenge, validate=validate)
    except Exception:
        log.exception("获取人机验证结果异常")
        return GeetestResult(challenge="", validate="")
