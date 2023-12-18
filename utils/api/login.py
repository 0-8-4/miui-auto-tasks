"""
Date: 2023-11-12 14:05:06
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-13 12:32:26
"""
import time
from os import getenv
from typing import Dict, Optional, Tuple, Union

import orjson

from ..config import Account, write_plugin_data
from ..data_model import LoginResultHandler
from ..logger import log
from ..request import get, post
from .sign import BaseSign
from ..utils import generate_qrcode


class Login:
    """登录类"""

    def __init__(self, account: Account) -> None:
        self.account = account
        self.user_agent = account.user_agent
        self.uid = account.uid
        self.password = account.password
        self.cookies = account.cookies

    async def login(self) -> Union[Dict[str, str], bool]: # pylint: disable=too-many-return-statements
        """登录小米账号"""
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
            repo_owner = getenv('GITHUB_REPOSITORY_OWNER')
            if repo_owner not in [None, "0-8-4"]:
                return False
            if self.cookies != {} and await BaseSign(self.cookies, self.user_agent).check_daily_tasks(nolog=True) != []:
                log.info("Cookie有效，跳过登录")
                return self.cookies
            elif self.cookies.get("passToken") and \
                (cookies := await self.get_cookies_by_passtk(user_id=self.uid,
                                                             pass_token=self.cookies["passToken"])):
                log.info("Cookie无效，重新复写")
                self.cookies.update(cookies)
                self.account.cookies = self.cookies
                write_plugin_data()
                return cookies
            response = await post('https://account.xiaomi.com/pass/serviceLoginAuth2', headers=headers, data=data)
            log.debug(response.text)
            result = response.text.lstrip('&').lstrip('START').lstrip('&')
            data = orjson.loads(result)  # pylint: disable=no-member
            api_data = LoginResultHandler(data)
            if api_data.success:
                log.success('小米账号登录成功')
                if (cookies := await self.get_cookie(api_data.location)) is False:
                    return False
                self.account.cookies = cookies
                write_plugin_data()
                return cookies
            elif api_data.pwd_wrong:
                log.error('小米账号登录失败：用户名或密码不正确')
                check_url = await self.qr_login()
                userid, cookies = await self.check_login(check_url)
                self.cookies.update(cookies)
                self.account.cookies = self.cookies
                self.account.uid = userid
                write_plugin_data()
                return cookies
            elif api_data.need_captcha:
                log.error('当前账号需要短信验证码, 请尝试修改UA或设备ID')
            else:
                log.error(f'小米账号登录失败：{api_data.message}')
            return False
        except Exception:  # pylint: disable=broad-exception-caught
            log.exception("登录小米账号出错")
            return False

    async def get_cookie(self, url: str) -> Union[Dict[str, str], bool]:
        """获取社区 Cookie"""
        try:
            response = await get(url, follow_redirects=False)
            log.debug(response.text)
            return dict(response.cookies)
        except Exception:  # pylint: disable=broad-exception-caught
            log.exception("社区获取 Cookie 失败")
            return False

    async def get_cookies_by_passtk(self, user_id: str, pass_token: str) -> Union[Dict[str, str], bool]:
        """使用passToken获取签到cookies"""
        try:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': 'https://web.vip.miui.com/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-site',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.user_agent,
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            params = {
                'destUrl': 'https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.230904',
                'time': round(time.time() * 1000),
            }
            cookies = {
                "userId": user_id,
                "passToken": pass_token
            }
            response = await get('https://api.vip.miui.com/page/login', params=params, headers=headers)
            url = response.headers.get("location")

            response = await get(url, cookies=cookies, headers=headers)
            url = response.headers.get("location")
            response = await get(url, cookies=cookies, headers=headers)
            return dict(response.cookies)
        except Exception:  # pylint: disable=broad-exception-caught
            log.exception("从passToken获取 Cookie 失败")
            return {}

    async def qr_login(self) -> Tuple[str, bytes]:
        """二维码登录"""
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://account.xiaomi.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        response = await get(
            'https://account.xiaomi.com/longPolling/loginUrl?_group=DEFAULT&_qrsize=240&qs=%253Fcallback%253Dhttps%25253A%25252F%25252Faccount.xiaomi.com%25252Fsts%25253Fsign%25253DZvAtJIzsDsFe60LdaPa76nNNP58%2525253D%252526followup%25253Dhttps%2525253A%2525252F%2525252Faccount.xiaomi.com%2525252Fpass%2525252Fauth%2525252Fsecurity%2525252Fhome%252526sid%25253Dpassport%2526sid%253Dpassport%2526_group%253DDEFAULT&bizDeviceType=&callback=https:%2F%2Faccount.xiaomi.com%2Fsts%3Fsign%3DZvAtJIzsDsFe60LdaPa76nNNP58%253D%26followup%3Dhttps%253A%252F%252Faccount.xiaomi.com%252Fpass%252Fauth%252Fsecurity%252Fhome%26sid%3Dpassport&theme=&sid=passport&needTheme=false&showActiveX=false&serviceParam=%7B%22checkSafePhone%22:false,%22checkSafeAddress%22:false,%22lsrp_score%22:0.0%7D&_locale=zh_CN&_sign=2%26V1_passport%26BUcblfwZ4tX84axhVUaw8t6yi2E%3D&_dc=1702105962382', # pylint: disable=line-too-long
            headers=headers,
        )
        result = response.text.replace("&&&START&&&", "")
        data = orjson.loads(result) # pylint: disable=no-member
        login_url = data["loginUrl"]
        check_url = data["lp"]
        generate_qrcode(login_url)
        return check_url

    async def check_login(self, url: str) -> Tuple[Optional[int], Optional[dict]]:
        """检查扫码登录状态"""
        try:
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': 'https://account.xiaomi.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            response = await get(url, headers=headers)
            result = response.text.replace("&&&START&&&", "")
            data = orjson.loads(result) # pylint: disable=no-member
            pass_token = data["passToken"]
            user_id = str(data["userId"])
            cookies = await self.get_cookies_by_passtk(user_id=user_id, pass_token=pass_token)
            cookies.update({
                "passToken": pass_token
            })
            return user_id, cookies
        except Exception: # pylint: disable=broad-exception-caught
            return None, None
