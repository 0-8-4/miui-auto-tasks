import time

from typing import Dict, List, Optional, Set, Type, Union

from ..data_model import ApiResultHandler, DailyTasksResult, SignResultHandler
from ..request import get, post
from ..logger import log


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

    def __init__(self, cookie: Dict, token: Optional[str] = None):
        self.cookie = cookie
        self.token = token
        self.headers = {
        }

    async def check_daily_tasks(self, nolog: bool=False) -> Union[List[DailyTasksResult], List[None]]:
        try:
            response = await get('https://api.vip.miui.com/mtop/planet/vip/member/getCheckinPageCakeList',
                                 cookies=self.cookie)
            log.debug(response.text)
            result = response.json()
            api_data = ApiResultHandler(result)
            if api_data.success:
                task_status = []
                task = next(filter(lambda x: x['head']['title'] == "每日任务", api_data.data))
                for daily_task in task['data']:
                    task_name = daily_task['title']
                    task_desc = daily_task.get('desc', '')
                    showType = True if daily_task['showType'] == 0 else False
                    task_status.append(DailyTasksResult(name=task_name, showType=showType, desc=task_desc))
                return task_status
            else:
                log.error("获取每日任务状态失败：" + api_data.message) if not nolog else None
                return []
        except Exception:
            log.exception("获取每日任务异常") if not nolog else None
            return []

    async def sign(self) -> bool:
        """
        每日任务处理器
        """
        try:
            params = self.PARAMS.copy()
            params['miui_vip_ph'] = self.cookie['miui_vip_ph'] if 'miui_vip_ph' in self.cookie else params
            params['token'] = self.token if 'token' in params else params
            data = self.DATA.copy()
            data['miui_vip_ph'] = self.cookie['miui_vip_ph'] if 'miui_vip_ph' in self.cookie else data
            data['token'] = self.token if 'token' in data else data
            response = await post(self.URL_SIGN,
                                  params=params, data=data,
                                  cookies=self.cookie, headers=self.headers)
            log.debug(response.text)
            result = response.json()
            api_data = SignResultHandler(result)
            if api_data:
                log.success(f"{self.NAME}结果: 成长值+" + api_data.growth)
                return True
            elif api_data.ck_invalid:
                log.error(f"{self.NAME}失败: Cookie无效")
                return False
            else:
                log.error(f"{self.NAME}失败：" + api_data.message)
                return False
        except Exception:
            log.exception(f"{self.NAME}出错")
            return False


class Check_In(BaseSign):
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
        'token': ""
    }
    URL_SIGN = 'https://api.vip.miui.com/mtop/planet/vip/user/checkinV2'


class Browse_Post(BaseSign):
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


class Browse_User_Page(BaseSign):
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


class Browse_Special_Page(BaseSign):
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


class Board_Follow(BaseSign):
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


class Board_UnFollow(BaseSign):
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


class Thumb_Up(BaseSign):
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


# 注册签到任务
BaseSign.AVAILABLE_SIGNS[Check_In.NAME] = Check_In
BaseSign.AVAILABLE_SIGNS[Browse_Post.NAME] = Browse_Post
BaseSign.AVAILABLE_SIGNS[Browse_User_Page.NAME] = Browse_User_Page
BaseSign.AVAILABLE_SIGNS[Browse_Special_Page.NAME] = Browse_Special_Page
BaseSign.AVAILABLE_SIGNS[Board_Follow.NAME] = Board_Follow
BaseSign.AVAILABLE_SIGNS[Board_UnFollow.NAME] = Board_UnFollow
BaseSign.AVAILABLE_SIGNS[Thumb_Up.NAME] = Thumb_Up
