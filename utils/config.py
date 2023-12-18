""""配置文件"""
import os
import platform
from hashlib import md5
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, List, Optional, Union

import orjson
import yaml # pylint: disable=wrong-import-order
from pydantic import BaseModel, ValidationError, field_validator # pylint: disable=no-name-in-module

from .logger import log

ROOT_PATH = Path(__file__).parent.parent.absolute()

DATA_PATH = ROOT_PATH / "data"
"""数据保存目录"""

CONFIG_TYPE = "json" if os.path.isfile(DATA_PATH / "config.json") else "yaml"
"""数据文件类型"""

CONFIG_PATH = DATA_PATH / f"config.{CONFIG_TYPE}" if os.getenv("MIUITASK_CONFIG_PATH") is None else Path(os.getenv("MIUITASK_CONFIG_PATH"))
"""数据文件默认路径"""

os.makedirs(DATA_PATH, exist_ok=True)


def md5_crypto(passwd: str) -> str:
    """MD5加密"""
    return md5(passwd.encode('utf8')).hexdigest().upper()


def cookies_to_dict(cookies: str):
    """将cookies字符串转换为字典"""
    cookies_dict = {}
    if not cookies or "=" not in cookies:
        return cookies_dict
    for cookie in cookies.split(';'):
        key, value = cookie.strip().split('=', 1)  # 分割键和值
        cookies_dict[key] = value
    return cookies_dict

def get_platform() -> str:
    """获取当前运行平台"""
    if os.path.exists('/.dockerenv'):
        if os.environ.get('QL_DIR') and os.environ.get('QL_BRANCH'):
            return "qinglong"
        else:
            return "docker"
    return platform.system().lower()


class Account(BaseModel):
    """账号处理器"""
    uid: str = "100000"
    """账户ID 非账户用户名或手机号"""
    password: str = ""
    """账户密码或其MD5哈希"""
    cookies: Union[dict, str] = {}
    """账户登录后的cookies"""
    user_agent: str = 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Safari/537.36'
    """登录社区时所用浏览器的 User-Agent"""

    CheckIn: bool = False
    """社区成长值签到，启用功能意味着你愿意自行承担相关风险"""
    BrowseUserPage: bool = False
    """社区浏览个人主页10秒，启用功能意味着你愿意自行承担相关风险"""
    BrowsePost: bool = False
    """社区浏览帖子10秒，启用功能意味着你愿意自行承担相关风险"""
    ThumbUp: bool = False
    """点赞帖子，启用功能意味着你愿意自行承担相关风险"""
    BrowseSpecialPage: bool = False
    """社区在活动期间可能会出现限时的“浏览指定专题页”任务，启用功能意味着你愿意自行承担相关风险"""
    BoardFollow: bool = False
    """社区可能会出现限时的“加入圈子”任务，启用功能意味着你愿意自行承担相关风险"""
    CarrotPull: bool = False
    """社区拔萝卜，启用功能意味着你愿意自行承担相关风险"""

    @field_validator("password")
    @classmethod
    def _password(cls, value: Optional[str]):  # pylint: disable=no-self-argument
        if len(value) == 32:
            return value
        return md5_crypto(value)

    @field_validator("cookies")
    @classmethod
    def _cookies(cls, value: Union[dict, str]):  # pylint: disable=no-self-argument
        if isinstance(value, str):
            return cookies_to_dict(value)
        return value


class OnePush(BaseModel):
    """推送配置"""
    notifier: Union[str, bool] = ""
    """是否开启消息推送"""
    params: Dict = {
        "title": "",
        "markdown": False,
        "token": "",
        "userid": ""
    }
    """推送参数"""


class Preference(BaseModel):
    """偏好设置"""
    geetest_url: str = ""
    """极验验证URL"""
    geetest_params: Dict = {}
    """极验自定义params参数"""
    geetest_data: Dict = {}
    """极验自定义data参数"""

class Config(BaseModel):
    """插件数据"""
    preference: Preference = Preference()
    """偏好设置"""
    accounts: List[Account] = [Account()]
    """账号设置"""
    ONEPUSH: OnePush = OnePush()
    """消息推送"""

def write_plugin_data(data: Config = None):
    """
    写入插件数据文件

    :param data: 配置对象
    """
    try:
        if data is None:
            data = ConfigManager.data_obj
        try:
            if CONFIG_TYPE == "json":
                str_data = orjson.dumps(data.model_dump(), option=orjson.OPT_PASSTHROUGH_DATETIME | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2)
                with open(CONFIG_PATH, "wb") as file:
                    file.write(str_data)
            else:
                str_data = yaml.dump(data.model_dump(), indent=4, allow_unicode=True, sort_keys=False)
                with open(CONFIG_PATH, "w", encoding="utf-8") as file:
                    file.write(str_data)
            return True
        except (AttributeError, TypeError, ValueError):
            log.exception("数据对象序列化失败，可能是数据类型错误")
            return False
    except OSError:
        return False


class ConfigManager:
    """配置管理器"""
    data_obj = Config()
    """加载出的插件数据对象"""
    platform = get_platform()
    """运行平台"""

    @classmethod
    def load_config(cls):
        """
        加载插件数据文件
        """
        if os.path.exists(DATA_PATH) and os.path.isfile(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r', encoding="utf-8") as file:
                    if CONFIG_TYPE == "json":
                        data = orjson.loads(file.read())
                    else:
                        data = yaml.safe_load(file)
                new_model = Config.model_validate(data)
                for attr in new_model.model_fields:
                    # ConfigManager.data_obj.__setattr__(attr, new_model.__getattribute__(attr))
                    setattr(ConfigManager.data_obj, attr, getattr(new_model, attr))
                write_plugin_data(ConfigManager.data_obj)  # 同步配置
            except (ValidationError, JSONDecodeError):
                log.exception(f"读取数据文件失败，请检查数据文件 {CONFIG_PATH} 格式是否正确")
                raise
            except Exception:
                log.exception(
                    f"读取数据文件失败，请检查数据文件 {CONFIG_PATH} 是否存在且有权限读取和写入")
                raise
        else:
            try:
                if not os.path.exists(DATA_PATH):
                    os.mkdir(DATA_PATH)
                write_plugin_data()
            except (AttributeError, TypeError, ValueError, PermissionError):
                log.exception(f"创建数据文件失败，请检查是否有权限读取和写入 {CONFIG_PATH}")
                raise
            log.info(f"数据文件 {CONFIG_PATH} 不存在，已创建默认数据文件。")


ConfigManager.load_config()
