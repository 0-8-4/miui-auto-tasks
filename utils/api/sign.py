"""
Date: 2023-12-03 02:07:29
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-01-19 17:03:47
"""

import time
from typing import Any, Dict, List, Optional, Tuple, Type

from requests_toolbelt import MultipartEncoder
from tenacity import RetryError, Retrying, stop_after_attempt

from ..config import Account
from ..data_model import (
    ApiResultHandler,
    DailyTasksResult,
    SignResultHandler,
    UserInfoResult,
)
from ..logger import log
from ..request import get, post
from ..utils import get_random_chars_as_string, is_incorrect_return


class BaseSign:
    """
    签到基类
    """

    NAME = ""
    """任务名字"""

    PARAMS = {}
    """签到参数"""

    DATA = {}
    """签到数据"""

    URL_SIGN = ""
    """签到地址"""

    AVAILABLE_SIGNS: Dict[str, Type["BaseSign"]] = {}
    """可用的子类"""

    def __init__(self, account: Account, token: Optional[str] = None):
        self.cookies = account.cookies
        self.token = token
        self.user_agent = account.user_agent
        self.headers = {
            "Host": "api-alpha.vip.miui.com",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": "Not_A",
            "Accept": "application/json",
            "sec-ch-ua-mobile": "?1",
            "User-Agent": self.user_agent,
            "sec-ch-ua-platform": "Android",
            "Origin": "https://web-alpha.vip.miui.com",
            "X-Requested-With": "com.xiaomi.vipaccount",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://web-alpha.vip.miui.com/",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        self.params = {
            "ref": "vipAccountShortcut",
            "pathname": "/mio/detail",
            "version": "dev.20231205",
            "miui_version": "V816.0.23.12.11.DEV",
            "android_version": "14",
            "oaid": {
                get_random_chars_as_string(16, "0123456789abcdefghijklmnopqrstuvwxyz")
            },
            "device": account.device,
            "restrict_imei": "",
            "miui_big_version": "V816",
            "model": account.device_model,
            "androidVersion": "14",
            "miuiBigVersion": "V816",
            "miui_vip_a_ph": None,
        }

    def check_daily_tasks(self, nolog: bool = False):
        """获取每日任务状态"""
        try:
            task_status: List[DailyTasksResult] = []
            for attempt in Retrying(stop=stop_after_attempt(3)):
                with attempt:
                    response = get(
                        "https://api-alpha.vip.miui.com/mtop/planet/vip/member/getCheckinPageCakeList",
                        cookies=self.cookies,
                    )
                    log.debug(response.text)
                    result = response.json()
                    api_data = ApiResultHandler(result)
                    if api_data.success:
                        tasks: List[Dict[str, List[Dict[str, Any]]]] = list(
                            filter(
                                lambda x: x["head"]["title"]
                                in ["每日任务", "其他任务"],
                                api_data.data,
                            )
                        )
                        for task in tasks:
                            for daily_task in task["data"]:
                                task_name = daily_task["title"]
                                task_desc = daily_task.get("desc", "")
                                show_type = daily_task["showType"] == 0
                                task_status.append(
                                    DailyTasksResult(
                                        name=task_name,
                                        showType=show_type,
                                        desc=task_desc,
                                    )
                                )
                        task_status.append(
                            DailyTasksResult(
                                name=WxSign.NAME,
                                showType=False,
                                desc=WxSign.NAME,
                            )
                        )
                        return task_status
                    else:
                        if not nolog:
                            log.error(f"获取每日任务状态失败：{api_data.message}")
            return task_status
        except RetryError as error:
            if is_incorrect_return(error):
                log.exception(f"每日任务 - 服务器没有正确返回 {response.text}")
            else:
                log.exception("获取每日任务异常")
            return task_status

    def sign(self) -> Tuple[bool, str]:  # pylint: disable=too-many-branches
        """
        每日任务处理器
        """
        try:
            for attempt in Retrying(stop=stop_after_attempt(3)):
                with attempt:
                    params = self.PARAMS.copy()
                    if "miui_vip_a_ph" in self.cookies:
                        params["miui_vip_a_ph"] = self.cookies["miui_vip_a_ph"]
                    if "token" in params:
                        params["token"] = self.token
                    self.params.update(params)
                    self.params["version"] = self.user_agent.split("/")[-1]

                    data = self.DATA.copy()
                    if "miui_vip_a_ph" in self.cookies:
                        data["miui_vip_a_ph"] = self.cookies["miui_vip_a_ph"]
                    if "token" in data:
                        if self.token:
                            data["token"] = self.token
                        else:
                            log.info(f"未获取到token, 跳过{self.NAME}")
                            return False, "None"
                    boundary = f'----WebKitFormBoundaryZ{get_random_chars_as_string(16, "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")}'
                    data = MultipartEncoder(fields=data, boundary=boundary)
                    self.headers["Content-Type"] = data.content_type
                    response = post(
                        self.URL_SIGN,
                        params=self.params,
                        data=data.to_string(),
                        cookies=self.cookies,
                        headers=self.headers,
                    )
                    log.debug(response.text)
                    result = response.json()
                    api_data = SignResultHandler(result)
                    if api_data:
                        if api_data.growth:
                            log.success(f"{self.NAME}结果: 成长值+{api_data.growth}")
                        else:
                            log.success(f"{self.NAME}结果: {api_data.message}")
                        return True, "None"
                    elif api_data.ck_invalid:
                        log.error(f"{self.NAME}失败: Cookie无效")
                        return False, "cookie"
                    else:
                        log.error(f"{self.NAME}失败：{api_data.message}")
                        return False, "None"
        except RetryError as error:
            if is_incorrect_return(error):
                log.exception(f"{self.NAME} - 服务器没有正确返回 {response.text}")
            else:
                log.exception("{self.NAME}出错")
            return False, "None"

    def user_info(self) -> UserInfoResult:
        """获取用户信息"""
        try:
            for attempt in Retrying(stop=stop_after_attempt(3)):
                with attempt:
                    headers = {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "User-Agent": self.user_agent,
                        "Request-Container-Mark": "android",
                        "Host": "api-alpha.vip.miui.com",
                        "Connection": "Keep-Alive",
                    }

                    response = get(
                        "https://api-alpha.vip.miui.com/mtop/planet/vip/homepage/mineInfo",
                        cookies=self.cookies,
                        headers=headers,
                    )
                    log.debug(response.text)
                    result = response.json()
                    api_data = ApiResultHandler(result)
                    if api_data.success:
                        return UserInfoResult(**api_data.data)
                    else:
                        log.error(f"获取用户信息失败：{api_data.message}")
                        return UserInfoResult()
        except RetryError as error:
            if is_incorrect_return(error):
                log.exception(f"用户信息 - 服务器没有正确返回 {response.text}")
            else:
                log.exception("获取用户信息异常")
            return UserInfoResult()


# pylint: disable=trailing-whitespace
class CheckIn(BaseSign):
    """
    每日签到
    """

    NAME = "每日签到"

    PARAMS = {
        "ref": "vipAccountShortcut",
        "pathname": "/mio/checkIn",
        "version": "dev.231026",
        "miui_vip_a_ph": "{miui_vip_a_ph}",
    }

    DATA = {"miui_vip_a_ph": "{miui_vip_a_ph}", "token": "{token}"}
    URL_SIGN = "https://api-alpha.vip.miui.com/mtop/planet/vip/user/checkinV2"


class BrowsePost(BaseSign):
    """
    浏览帖子超过10秒
    """

    NAME = "浏览帖子超过10秒"

    PARAMS = {
        "ref": "vipAccountShortcut",
        "pathname": "/mio/detail",
        "version": "dev.231026",
        "miui_vip_a_ph": "{miui_vip_a_ph}",
    }
    DATA = {"action": "BROWSE_POST_10S", "miui_vip_a_ph": "{miui_vip_a_ph}"}
    URL_SIGN = "https://api-alpha.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByActionV2"


class BrowseUserPage(BaseSign):
    """
    浏览个人主页10s
    """

    NAME = "浏览个人主页10s"

    PARAMS = {
        "ref": "vipAccountShortcut",
        "pathname": "/mio/detail",
        "version": "dev.231026",
        "miui_vip_a_ph": "{miui_vip_a_ph}",
    }
    DATA = {
        "action": "BROWSE_SPECIAL_PAGES_USER_HOME",
        "miui_vip_a_ph": "{miui_vip_a_ph}",
    }
    URL_SIGN = "https://api-alpha.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByActionV2"


class BrowseSpecialPage(BaseSign):
    """
    浏览指定专题页
    """

    NAME = "浏览指定专题页"

    PARAMS = {
        "ref": "vipAccountShortcut",
        "pathname": "/mio/detail",
        "version": "dev.231026",
        "miui_vip_a_ph": "{miui_vip_a_ph}",
    }
    DATA = {
        "action": "BROWSE_SPECIAL_PAGES_SPECIAL_PAGE",
        "miui_vip_a_ph": "{miui_vip_a_ph}",
    }
    URL_SIGN = "https://api-alpha.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByActionV2"


class BrowseVideoPost(BaseSign):
    """
    浏览指定页面的多个视频超过5分钟（中途退出重新计算时间）
    """

    NAME = "浏览指定页面的多个视频超过5分钟（中途退出重新计算时间）"

    PARAMS = {
        "ref": "vipAccountShortcut",
        "pathname": "/mio/detail",
        "version": "dev.231026",
        "miui_vip_a_ph": "{miui_vip_a_ph}",
    }
    DATA = {"action": "BROWSE_VIDEO_POST", "miui_vip_a_ph": "{miui_vip_a_ph}"}
    URL_SIGN = "https://api-alpha.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByActionV2"


class BoardFollow(BaseSign):
    """
    加入小米圈子
    """

    NAME = "加入小米圈子"

    PARAMS = {
        "pathname": "/mio/allboard",
        "version": "dev.20051",
        "boardId": "558495",
        "miui_vip_a_ph": "{miui_vip_a_ph}",
    }

    URL_SIGN = "https://api-alpha.vip.miui.com/api/community/board/follow"


class BoardUnFollow(BaseSign):
    """
    退出小米圈子
    """

    NAME = "退出小米圈子"

    PARAMS = {
        "pathname": "/mio/allboard",
        "version": "dev.20051",
        "boardId": "558495",
        "miui_vip_a_ph": "{miui_vip_a_ph}",
    }

    URL_SIGN = "https://api-alpha.vip.miui.com/api/community/board/unfollow"


class ThumbUp(BaseSign):
    """
    点赞他人帖子
    """

    NAME = "点赞他人帖子"

    DATA = {
        "postId": "36625780",
        "sign": "36625780",
        "timestamp": int(round(time.time() * 1000)),
    }

    URL_SIGN = "https://api-alpha.vip.miui.com/mtop/planet/vip/content/announceThumbUp"


class CarrotPull(BaseSign):
    """
    参与拔萝卜获得奖励
    """

    NAME = "参与拔萝卜获得奖励"
    DATA = {"miui_vip_a_ph": "{miui_vip_a_ph}"}
    URL_SIGN = "https://api-alpha.vip.miui.com/api/carrot/pull"


class WxSign(BaseSign):
    """
    微信签到
    """

    NAME = "微信小程序签到"
    PARAMS = {"miui_vip_a_ph": "{miui_vip_a_ph}"}
    DATA = {"action": "WECHAT_CHECKIN_TASK"}
    URL_SIGN = "https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByActionV2"


# 注册签到任务
BaseSign.AVAILABLE_SIGNS[WxSign.NAME] = WxSign
BaseSign.AVAILABLE_SIGNS[CheckIn.NAME] = CheckIn
BaseSign.AVAILABLE_SIGNS[BrowsePost.NAME] = BrowsePost
BaseSign.AVAILABLE_SIGNS[BrowseVideoPost.NAME] = BrowseVideoPost
BaseSign.AVAILABLE_SIGNS[BrowseUserPage.NAME] = BrowseUserPage
BaseSign.AVAILABLE_SIGNS[BrowseSpecialPage.NAME] = BrowseSpecialPage
BaseSign.AVAILABLE_SIGNS[BoardFollow.NAME] = BoardFollow
BaseSign.AVAILABLE_SIGNS[BoardUnFollow.NAME] = BoardUnFollow
BaseSign.AVAILABLE_SIGNS[ThumbUp.NAME] = ThumbUp
BaseSign.AVAILABLE_SIGNS[CarrotPull.NAME] = CarrotPull
