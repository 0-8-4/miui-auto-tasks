'''
Date: 2023-11-13 19:55:22
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-13 20:57:08
'''

from .request import get, post
from .logger import log
from .data_model import ApiResultHandler, GeetestResult

async def get_validate(gt: str, challenge: str) -> GeetestResult:
    validate = ""
    try:
        return GeetestResult(challenge=challenge, validate=validate)
    except Exception:
        log.exception("获取人机验证结果异常")
        return GeetestResult(challenge="", validate="")
