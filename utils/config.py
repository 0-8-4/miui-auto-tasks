""""配置文件"""

import json
import os
import platform
from hashlib import md5
from pathlib import Path
from typing import Literal, Optional

import yaml  # pylint: disable=wrong-import-order

from .logger import log

ROOT_PATH = Path(__file__).parent.parent.absolute()

DATA_PATH = ROOT_PATH / "data"
"""数据保存目录"""

CONFIG_TYPE = "json" if os.path.isfile(DATA_PATH / "config.json") else "yaml"
"""数据文件类型"""

CONFIG_PATH = (
    DATA_PATH / f"config.{CONFIG_TYPE}"
    if os.getenv("MIUITASK_CONFIG_PATH") is None
    else Path(str(os.getenv("MIUITASK_CONFIG_PATH")))
)
"""数据文件默认路径"""

os.makedirs(DATA_PATH, exist_ok=True)


def md5_crypto(passwd: str) -> str:
    """MD5加密"""
    return md5(passwd.encode("utf8")).hexdigest().upper()


def cookies_to_dict(cookies: str):
    """将cookies字符串转换为字典"""
    cookies_dict = {}
    if not cookies or "=" not in cookies:
        return cookies_dict
    for cookie in cookies.split(";"):
        key, value = cookie.strip().split("=", 1)  # 分割键和值
        cookies_dict[key] = value
    return cookies_dict


def get_platform() -> str:
    """获取当前运行平台"""
    if os.path.exists("/.dockerenv"):
        if os.environ.get("QL_DIR") and os.environ.get("QL_BRANCH"):
            return "qinglong"
        else:
            return "docker"
    return platform.system().lower()


# pylint: disable=too-many-instance-attributes
class Account:
    """账号处理器"""

    # pylint: disable=too-many-arguments, too-many-positional-arguments, too-many-locals
    def __init__(
        self,
        uid="100000",
        password="",
        cookies=None,
        login_user_agent="",
        user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Safari/537.36",
        device="",
        device_model="",
        CheckIn=False,
        BrowseUserPage=False,
        BrowsePost=False,
        BrowseVideoPost=False,
        ThumbUp=False,
        BrowseSpecialPage=False,
        BoardFollow=False,
        CarrotPull=False,
        WxSign=False,
    ):
        self.uid = uid
        """账户ID 非账户用户名或手机号"""
        self.password = password
        """账户密码或其MD5哈希"""
        self.cookies = cookies or {}
        """账户登录后的cookies"""
        self.login_user_agent = login_user_agent
        """登录账户时所用浏览器的 User-Agent"""
        self.user_agent = user_agent
        """登录社区时所用浏览器的 User-Agent"""
        self.device = device
        """设备代号"""
        self.device_model = device_model
        """设备名称"""
        self.CheckIn = CheckIn
        """社区成长值签到，启用功能意味着你愿意自行承担相关风险"""
        self.BrowseUserPage = BrowseUserPage
        """社区浏览个人主页10秒，启用功能意味着你愿意自行承担相关风险"""
        self.BrowsePost = BrowsePost
        """社区浏览帖子10秒，启用功能意味着你愿意自行承担相关风险"""
        self.BrowseVideoPost = BrowseVideoPost
        """社区浏览视频帖子5分钟，启用功能意味着你愿意自行承担相关风险"""
        self.ThumbUp = ThumbUp
        """点赞帖子，启用功能意味着你愿意自行承担相关风险"""
        self.BrowseSpecialPage = BrowseSpecialPage
        """社区在活动期间可能会出现限时的“浏览指定专题页”任务，启用功能意味着你愿意自行承担相关风险"""
        self.BoardFollow = BoardFollow
        """社区可能会出现限时的“加入圈子”任务，启用功能意味着你愿意自行承担相关风险"""
        self.CarrotPull = CarrotPull
        """社区拔萝卜，启用功能意味着你愿意自行承担相关风险"""
        self.WxSign = WxSign
        """微信小程序签到，启用功能意味着你愿意自行承担相关风险"""

    def _password(self):
        if len(self.password) == 32:
            return self.password
        return md5_crypto(self.password)

    def _cookies(self):
        if isinstance(self.cookies, str):
            return cookies_to_dict(self.cookies)
        return self.cookies


class OnePush:
    """推送配置"""

    def __init__(self, notifier="", params=None):
        self.notifier = notifier
        self.params = params or {
            "title": "",
            "markdown": False,
            "token": "",
            "userid": "",
        }


class Preference:
    """偏好设置"""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        geetest_url="",
        geetest_method: Literal["post", "get"] = "post",
        geetest_params: Optional[dict] = None,
        geetest_data: Optional[dict] = None,
        geetest_validate_path="$.data.validate",
        geetest_challenge_path="$.data.challenge",
        get_geetest_url="",
        get_geetest_method: Literal["post", "get"] = "post",
        get_geetest_params: Optional[dict] = None,
        get_geetest_data: Optional[dict] = None,
        get_geetest_validate_path="",
        get_geetest_challenge_path="",
    ):
        self.geetest_url = geetest_url
        """极验验证URL"""
        self.geetest_method = geetest_method
        """极验请求方法"""
        self.geetest_params = geetest_params or {}
        """极验自定义params参数"""
        self.geetest_data = geetest_data or {}
        """极验自定义data参数"""
        self.geetest_validate_path = geetest_validate_path
        """极验验证validate的路径"""
        self.geetest_challenge_path = geetest_challenge_path
        """极验验证challenge的路径"""
        self.get_geetest_url = get_geetest_url
        """获取极验验证结果的URL"""
        self.get_geetest_method = get_geetest_method
        """获取极验验证结果的请求方法"""
        self.get_geetest_params = get_geetest_params or {}
        """获取极验验证结果的自定义params参数"""
        self.get_geetest_data = get_geetest_data or {}
        """获取极验验证结果的自定义data参数"""
        self.get_geetest_validate_path = get_geetest_validate_path
        """获取极验验证validate的路径"""
        self.get_geetest_challenge_path = get_geetest_challenge_path
        """获取极验验证challenge的路径"""


class Config:
    """插件数据"""

    def __init__(self, preference=None, accounts=None, onepush=None):
        self.preference = preference or Preference()
        self.accounts = accounts or [Account()]
        self.ONEPUSH = onepush or OnePush()

    def to_dict(self):
        """将 Config 转换为字典"""
        return {
            "preference": vars(self.preference),
            "accounts": [vars(account) for account in self.accounts],
            "ONEPUSH": vars(self.ONEPUSH),
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建 Config 实例"""
        preference = Preference(**data.get("preference", {}))
        accounts = [Account(**account) for account in data.get("accounts", [])]
        onepush = OnePush(**data.get("ONEPUSH", {}))
        return cls(preference, accounts, onepush)


class ConfigManager:
    """配置管理器"""

    data_obj = Config()
    platform = "platform_example"  # 示例平台

    @classmethod
    def load_config(cls):
        """
        加载插件数据文件
        """
        if os.path.exists(CONFIG_PATH) and os.path.isfile(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as file:
                    if CONFIG_TYPE == "json":
                        data = json.load(file)
                    else:
                        data = yaml.safe_load(file)
                # 从文件数据创建 Config 对象
                cls.data_obj = Config.from_dict(data)
                cls.write_plugin_data(cls.data_obj)  # 同步配置
            except Exception as e:
                log.exception(f"读取数据文件失败，请检查文件格式或权限: {e}")
                raise
        else:
            try:
                if not os.path.exists(DATA_PATH):
                    os.mkdir(DATA_PATH)
                cls.write_plugin_data(cls.data_obj)  # 创建并写入默认数据
            except Exception as e:
                log.exception(f"创建数据文件失败，请检查权限: {e}")
                raise
            log.info(f"数据文件 {CONFIG_PATH} 不存在，已创建默认数据文件。")

    @classmethod
    def write_plugin_data(cls, data: Config = None):
        """
        写入插件数据文件
        :param data: 配置对象
        """
        try:
            if data is None:
                data = cls.data_obj
            if CONFIG_TYPE == "json":
                with open(CONFIG_PATH, "w", encoding="utf-8") as file:
                    json.dump(data.to_dict(), file, indent=4, ensure_ascii=False)
            else:
                with open(CONFIG_PATH, "w", encoding="utf-8") as file:
                    yaml.dump(
                        data.to_dict(),
                        file,
                        indent=4,
                        allow_unicode=True,
                        sort_keys=False,
                    )
            return True
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            log.exception(f"写入数据文件失败: {e}")
            return False


# 加载配置
ConfigManager.load_config()
