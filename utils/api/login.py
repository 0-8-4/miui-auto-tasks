"""
Date: 2023-11-12 14:05:06
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-13 12:32:26
"""
import orjson

from typing import Dict, List, Optional, Union

from ..config import Account, write_plugin_data
from ..request import get, post
from ..logger import log
from ..data_model import LoginResultHandler
from .sign import BaseSign


class Login:
    def __init__(self, account: Account) -> None:
        self.account = account
        self.user_agent = account.user_agent
        self.uid = account.uid
        self.password = account.password
        self.cookies = account.cookies

    async def login(self) -> Union[Dict[str, str], bool]:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://account.xiaomi.com/fe/service/login/password?sid=miui_vip&qs=%253Fcallback%253Dhttp'
                       '%25253A%25252F%25252Fapi.vip.miui.com%25252Fsts%25253Fsign%25253D4II4ABwZkiJzkd2YSkyEZukI4Ak'
                       '%2525253D%252526followup%25253Dhttps%2525253A%2525252F%2525252Fapi.vip.miui.com%2525252Fpage'
                       '%2525252Flogin%2525253FdestUrl%2525253Dhttps%252525253A%252525252F%252525252Fweb.vip.miui.com'
                       '%252525252Fpage%252525252Finfo%252525252Fmio%252525252Fmio%252525252FinternalTest%252525253Fref'
                       '%252525253Dhomepage%2526sid%253Dmiui_vip&callback=http%3A%2F%2Fapi.vip.miui.com%2Fsts%3Fsign'
                       '%3D4II4ABwZkiJzkd2YSkyEZukI4Ak%253D%26followup%3Dhttps%253A%252F%252Fapi.vip.miui.com%252Fpage'
                       '%252Flogin%253FdestUrl%253Dhttps%25253A%25252F%25252Fweb.vip.miui.com%25252Fpage%25252Finfo'
                       '%25252Fmio%25252Fmio%25252FinternalTest%25253Fref%25253Dhomepage&_sign=L%2BdSQY6sjSQ%2FCRjJs4p'
                       '%2BU1vNYLY%3D&serviceParam=%7B%22checkSafePhone%22%3Afalse%2C%22checkSafeAddress%22%3Afalse%2C'
                       '%22lsrp_score%22%3A0.0%7D&showActiveX=false&theme=&needTheme=false&bizDeviceType=',
            'User-Agent': str(self.user_agent),
            'Origin': 'https://account.xiaomi.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'deviceId=; pass_ua=web; uLocale=zh_CN'
        }
        data = {
            'bizDeviceType': '',
            'needTheme': 'false',
            'theme': '',
            'showActiveX': 'false',
            'serviceParam': '{"checkSafePhone":false,"checkSafeAddress":false,"lsrp_score":0.0}',
            'callback': 'http://api.vip.miui.com/sts?sign=4II4ABwZkiJzkd2YSkyEZukI4Ak%3D&followup=https%3A%2F%2Fapi.vip'
                        '.miui.com%2Fpage%2Flogin%3FdestUrl%3Dhttps%253A%252F%252Fweb.vip.miui.com%252Fpage%252Finfo'
                        '%252Fmio%252Fmio%252FinternalTest%253Fref%253Dhomepage',
            'qs': '%3Fcallback%3Dhttp%253A%252F%252Fapi.vip.miui.com%252Fsts%253Fsign%253D4II4ABwZkiJzkd2YSkyEZukI4Ak'
                  '%25253D%2526followup%253Dhttps%25253A%25252F%25252Fapi.vip.miui.com%25252Fpage%25252Flogin'
                  '%25253FdestUrl%25253Dhttps%2525253A%2525252F%2525252Fweb.vip.miui.com%2525252Fpage%2525252Finfo'
                  '%2525252Fmio%2525252Fmio%2525252FinternalTest%2525253Fref%2525253Dhomepage%26sid%3Dmiui_vip',
            'sid': 'miui_vip',
            '_sign': 'L+dSQY6sjSQ/CRjJs4p+U1vNYLY=',
            'user': str(self.uid),
            'cc': '+86',
            'hash': str(self.password),
            '_json': 'true'
        }
        try:
            if self.cookies != {} and await BaseSign(self.cookies).check_daily_tasks(nolog=True) != []:
                log.info("Cookie有效，跳过登录")
                return self.cookies
            response = await post('https://account.xiaomi.com/pass/serviceLoginAuth2', headers=headers, data=data)
            log.debug(response.text)
            result = response.text.lstrip('&').lstrip('START').lstrip('&')
            data = orjson.loads(result)
            api_data = LoginResultHandler(data)
            if api_data.success:
                log.success('小米账号登录成功')
                cookies = await self.get_cookie(api_data.location)
                self.account.cookies = cookies
                write_plugin_data()
                return cookies
            elif not api_data.pwd_wrong:
                log.error('小米账号登录失败：' + api_data.message)
                return False
            elif api_data.need_captcha:
                log.error('当前账号需要短信验证码, 请尝试修改UA或设备ID')
                return False
            else:
                log.error('小米账号登录失败：用户名或密码不正确')
                return False
        except Exception:
            log.exception("登录小米账号出错")
            return False

    async def get_cookie(self, url: str) -> Union[Dict[str, str], bool]:
        try:
            response = await get(url, follow_redirects=False)
            log.debug(response.text)
            return dict(response.cookies)
        except Exception:
            log.exception("社区获取 Cookie 失败")
            return False
