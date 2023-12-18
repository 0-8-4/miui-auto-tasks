"""签到实例"""

import time

from typing import Dict, List, Optional, Type, Union, Any, Tuple
from tenacity import RetryError, Retrying, stop_after_attempt

from ..data_model import ApiResultHandler, DailyTasksResult, SignResultHandler, UserInfoResult
from ..request import get, post
from ..logger import log
from ..utils import is_incorrect_return


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

    def __init__(self, cookies: Dict, user_agent: str, token: Optional[str] = None):
        self.cookies = cookies
        self.token = token
        self.user_agent = user_agent
        self.headers = {
        }

    async def check_daily_tasks(self, nolog: bool = False) -> Union[List[DailyTasksResult], List[None]]:
        """获取每日任务状态"""
        try:
            for attempt in Retrying(stop=stop_after_attempt(3)):
                with attempt:
                    response = await get('https://api.vip.miui.com/mtop/planet/vip/member/getCheckinPageCakeList',
                                        cookies=self.cookies)
                    log.debug(response.text)
                    result = response.json()
                    api_data = ApiResultHandler(result)
                    if api_data.success:
                        task_status = []
                        tasks: List[Dict[str, List[Dict[str, Any]]]] = list(filter(
                            lambda x: x['head']['title'] in ["每日任务", "其他任务"], api_data.data))
                        for task in tasks:
                            for daily_task in task['data']:
                                task_name = daily_task['title']
                                task_desc = daily_task.get('desc', '')
                                show_type = True if daily_task['showType'] == 0 else False  # pylint: disable=simplifiable-if-expression
                                task_status.append(DailyTasksResult(name=task_name, showType=show_type, desc=task_desc))
                        return task_status
                    else:
                        if not nolog:
                            log.error(f"获取每日任务状态失败：{api_data.message}")
                    return []
        except RetryError as error:
            if is_incorrect_return(error):
                log.exception(f"每日任务 - 服务器没有正确返回 {response.text}")
            else:
                log.exception("获取每日任务异常")
            return []

    async def sign(self) -> Tuple[bool, str]:
        """
        每日任务处理器
        """
        try:
            for attempt in Retrying(stop=stop_after_attempt(3)):
                with attempt:
                    params = self.PARAMS.copy()
                    params['miui_vip_ph'] = self.cookies['miui_vip_ph'] if 'miui_vip_ph' in self.cookies else params
                    params['token'] = self.token if 'token' in params else params
                    data = self.DATA.copy()
                    data['miui_vip_ph'] = self.cookies['miui_vip_ph'] if 'miui_vip_ph' in self.cookies else data
                    if 'token' in data:
                        if self.token:
                            data['token'] = self.token
                        else:
                            log.info(f"未获取到token, 跳过{self.NAME}")
                            return False, "None"
                    response = await post(self.URL_SIGN,
                                        params=params, data=data,
                                        cookies=self.cookies, headers=self.headers)
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

    async def user_info(self) -> UserInfoResult:
        """获取用户信息"""
        try:
            for attempt in Retrying(stop=stop_after_attempt(3)):
                with attempt:
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent': self.user_agent,
                        'Request-Container-Mark': 'android',
                        'Host': 'api.vip.miui.com',
                        'Connection': 'Keep-Alive',
                    }

                    response = await get(
                        'https://api.vip.miui.com/mtop/planet/vip/homepage/mineInfo',
                        cookies=self.cookies,
                        headers=headers,
                    )
                    log.debug(response.text)
                    result = response.json()
                    api_data = ApiResultHandler(result)
                    if api_data.success:
                        return UserInfoResult.model_validate(api_data.data)
                    else:
                        log.error(f"获取用户信息失败：{api_data.message}")
                        return UserInfoResult()
        except RetryError as error:
            if is_incorrect_return(error):
                log.exception(f"用户信息 - 服务器没有正确返回 {response.text}")
            else:
                log.exception("获取用户信息异常")
            return UserInfoResult()
#pylint: disable=trailing-whitespace
class CheckIn(BaseSign):
    """
    每日签到
    """
    NAME = "每日签到"

    PARAMS = {
        'ref': 'vipAccountShortcut',
        'pathname': '/mio/checkIn',
        'version': 'dev.231026',
        'miui_vip_ph': "{miui_vip_ph}"
    }

    DATA = {
        'miui_vip_ph': "{miui_vip_ph}",
        'token': "{token}"
    }
    URL_SIGN = 'https://api.vip.miui.com/mtop/planet/vip/user/checkinV2'


class BrowsePost(BaseSign):
    """
    浏览帖子超过10秒
    """
    NAME = "浏览帖子超过10秒"

    PARAMS = {
        'ref': 'vipAccountShortcut',
        'pathname': '/mio/detail',
        'version': 'dev.231026',
        'miui_vip_ph': "{miui_vip_ph}"
    }
    DATA = {
        'action': 'BROWSE_POST_10S',
        'miui_vip_ph': "{miui_vip_ph}"
    }
    URL_SIGN = 'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByActionV2'


class BrowseUserPage(BaseSign):
    """
    浏览个人主页10s
    """
    NAME = "浏览个人主页10s"

    PARAMS = {
        'ref': 'vipAccountShortcut',
        'pathname': '/mio/detail',
        'version': 'dev.231026',
        'miui_vip_ph': "{miui_vip_ph}"
    }
    DATA = {
        'action': 'BROWSE_SPECIAL_PAGES_USER_HOME',
        'miui_vip_ph': "{miui_vip_ph}"
    }
    URL_SIGN = 'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByActionV2'


class BrowseSpecialPage(BaseSign):
    """
    浏览指定专题页
    """
    NAME = "浏览指定专题页"

    PARAMS = {
        'ref': 'vipAccountShortcut',
        'pathname': '/mio/detail',
        'version': 'dev.231026',
        'miui_vip_ph': "{miui_vip_ph}"
    }
    DATA = {
        'action': 'BROWSE_SPECIAL_PAGES_SPECIAL_PAGE',
        'miui_vip_ph': "{miui_vip_ph}"
    }
    URL_SIGN = 'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByActionV2'


class BoardFollow(BaseSign):
    """
    加入小米圈子
    """
    NAME = "加入小米圈子"

    PARAMS = {
        'pathname': '/mio/allboard',
        'version': 'dev.20051',
        'boardId': '558495',
        'miui_vip_ph': "{miui_vip_ph}"
    }

    URL_SIGN = 'https://api.vip.miui.com/api/community/board/follow'


class BoardUnFollow(BaseSign):
    """
    退出小米圈子
    """
    NAME = "退出小米圈子"

    PARAMS = {
        'pathname': '/mio/allboard',
        'version': 'dev.20051',
        'boardId': '558495',
        'miui_vip_ph': "{miui_vip_ph}"
    }

    URL_SIGN = 'https://api.vip.miui.com/api/community/board/unfollow'


class ThumbUp(BaseSign):
    """
    点赞他人帖子
    """
    NAME = "点赞他人帖子"

    DATA = {
        'postId': '36625780',
        'sign': '36625780',
        'timestamp': int(round(time.time() * 1000))
    }

    URL_SIGN = 'https://api.vip.miui.com/mtop/planet/vip/content/announceThumbUp'


class CarrotPull(BaseSign):
    """
    参与拔萝卜获得奖励
    """
    NAME = "参与拔萝卜获得奖励"
    DATA = {
        'miui_vip_ph': "{miui_vip_ph}"
    }
    URL_SIGN = 'https://api.vip.miui.com/api/carrot/pull'


# 注册签到任务
BaseSign.AVAILABLE_SIGNS[CheckIn.NAME] = CheckIn
BaseSign.AVAILABLE_SIGNS[BrowsePost.NAME] = BrowsePost
BaseSign.AVAILABLE_SIGNS[BrowseUserPage.NAME] = BrowseUserPage
BaseSign.AVAILABLE_SIGNS[BrowseSpecialPage.NAME] = BrowseSpecialPage
BaseSign.AVAILABLE_SIGNS[BoardFollow.NAME] = BoardFollow
BaseSign.AVAILABLE_SIGNS[BoardUnFollow.NAME] = BoardUnFollow
BaseSign.AVAILABLE_SIGNS[ThumbUp.NAME] = ThumbUp
BaseSign.AVAILABLE_SIGNS[CarrotPull.NAME] = CarrotPull
