"""
数据模型
"""
from typing import Any, Dict, NamedTuple, Optional


class ApiResultHandler:
    """
    API返回的数据处理器
    """
    def __init__(self, content: Dict[str, Any]):
        """
        初始化处理器，解析API返回的数据。

        :param content: API返回的原始JSON对象
        """
        self.content = content
        self.data: Dict[str, str] = self.content.get("data", {})
        self.message: str = self.content.get("message", "")
        self.status = self.content.get("status")

        # 尝试从其他键获取数据
        for key in ["data", "entity"]:
            if self.data == {}:
                self.data = self.content.get(key, {})
            else:
                break

        for key in ["code", "status"]:
            if self.status is None:
                self.status = self.content.get(key)
                if self.status is None and isinstance(self.data, dict):
                    self.status = self.data.get(key)

        for key in ["desc", "message"]:
            if self.message == "":
                self.message = self.content.get(key, "")
                if self.message is None and isinstance(self.data, dict):
                    self.message = self.data.get(key, "")

    @property
    def success(self):
        """
        是否成功
        """
        return (self.status in [0, 200] or self.message in ["成功", "OK", "success"]) and not self.content.get("notificationUrl")


class LoginResultHandler(ApiResultHandler):
    """
    登录API返回的数据处理器
    """
    def __init__(self, content: Dict[str, Any]):
        super().__init__(content=content)

        self.pwd = self.content.get("pwd")
        self.location = self.content.get("location")
        self.pass_token = self.content.get("passToken")
        self.user_id = str(self.content.get("userId"))

    @property
    def need_captcha(self):
        """
        是否需要验证码
        """
        return self.status == 87001 or "验证码" in self.message or self.content.get("notificationUrl")

    @property
    def pwd_wrong(self):
        """
        密码错误
        """
        return self.status == 70016


class DailyTasksResult(NamedTuple):
    """
    每日任务API返回的数据处理器
    """
    name: str
    """任务名称"""
    showType: bool
    """任务状态"""
    desc: Optional[str]
    """任务描述"""


class SignResultHandler(ApiResultHandler):
    """
    签到API返回的数据处理器
    """

    def __init__(self, content: Dict[str, Any]):
        super().__init__(content=content)
        self.growth = self.content.get("entity", {})
        if isinstance(self.growth, dict):
            self.growth = self.growth.get("score")
        elif isinstance(self.growth, int):
            self.growth = str(self.growth)
        else:
            self.growth = None

    def __bool__(self):
        """
        签到是否成功
        """
        return self.success

    @property
    def ck_invalid(self):
        """
        cookie是否失效
        """
        return self.status == 401


class TokenResultHandler(ApiResultHandler):
    """
    TOKEN数据处理器
    """
    def __init__(self, content: Dict[str, Any]):
        super().__init__(content=content)
        self.token = self.data.get("token", "")

    @property
    def need_verify(self):
        """需要验证码"""
        return self.data.get("result") is False and self.data.get("url")

    @property
    def success(self):
        """是否成功获取TOKEN"""
        return self.token != ""


class GeetestResult(NamedTuple):
    """人机验证结果数据"""
    validate: str
    challenge: str


class UserInfoResult:
    """用户信息数据"""
    def __init__(self, **kwargs):
        """
        初始化用户信息对象

        :param kwargs: 用户信息字典，包含了 'userInfo' 和 'userGrowLevelInfo'
        """
        if isinstance(kwargs, dict) and kwargs:
            kwargs = kwargs.get("userInfo", {}).get("userGrowLevelInfo", {})
            self.title = kwargs.get("title", "未知")
            self.point = kwargs.get("point", 0)
        else:
            self.title = "未知"
            self.point = 0
