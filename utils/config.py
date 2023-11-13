import os
import orjson
from pathlib import Path
from typing import Dict, List, Optional
from hashlib import md5

import yaml
from loguru import logger as log
from orjson import JSONDecodeError
from pydantic import BaseModel, ValidationError, validator

ROOT_PATH = Path(__name__).parent.absolute()

DATA_PATH = ROOT_PATH / "data"
'''数据保存目录'''

CONFIG_PATH = DATA_PATH / "config.yaml"
"""数据文件默认路径"""

def md5_crypto(passwd: str) -> str:
    return md5(passwd.encode('utf8')).hexdigest().upper()

class Account(BaseModel):
    uid: str = "100000"
    """账户ID 非账户用户名或手机号"""
    password: str = ""
    """账户密码或其MD5哈希"""
    user_agent: str = 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Safari/537.36'
    """登录社区时所用浏览器的 User-Agent"""

    """功能开关"""
    Check_In: bool = False
    """社区成长值签到，启用功能意味着你愿意自行承担相关风险"""
    Browse_User_Page: bool = False
    """社区浏览个人主页10秒，启用功能意味着你愿意自行承担相关风险"""
    Browse_Post: bool = False
    """社区浏览帖子10秒，启用功能意味着你愿意自行承担相关风险"""
    Thumb_Up: bool = False
    """点赞帖子，启用功能意味着你愿意自行承担相关风险"""
    Browse_Special_Page: bool = False
    """社区在活动期间可能会出现限时的“浏览指定专题页”任务，启用功能意味着你愿意自行承担相关风险"""
    Board_Follow: bool = False
    """社区可能会出现限时的“加入圈子”任务，启用功能意味着你愿意自行承担相关风险"""
    carrot_pull: bool = False
    """社区拔萝卜，启用功能意味着你愿意自行承担相关风险"""

    @validator("password", allow_reuse=True)
    def _(cls, v: Optional[str]):
        if len(v) == 32:
            return v
        return md5_crypto(v)
    
class OnePush(BaseModel):
    notifier: str = ""
    """是否开启消息推送"""
    params: Dict = {
            "title": "",
            "markdown": False,
            "token": "",
            "userid": ""
        }
    """推送参数"""

class Config(BaseModel):
    accounts: List[Account] = [Account()]
    """偏好设置"""
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
            #str_data = orjson.dumps(data.dict(), option=orjson.OPT_PASSTHROUGH_DATETIME | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2)
            str_data = yaml.dump(data.model_dump(), indent=4, allow_unicode=True, sort_keys=False)
        except (AttributeError, TypeError, ValueError):
            log.exception("数据对象序列化失败，可能是数据类型错误")
            return False
        with open(CONFIG_PATH, "w") as f:
            f.write(str_data)
        return True
    except OSError:
        return False

class ConfigManager:
    data_obj = Config()
    """加载出的插件数据对象"""
    platform = "pc"
    """运行环境"""

    @classmethod
    def load_config(cls):
        """
        加载插件数据文件
        """
        if os.path.exists(DATA_PATH) and os.path.isfile(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as file:
                    data = yaml.safe_load(file)
                new_model = Config.model_validate(data)
                for attr in new_model.model_fields:
                    ConfigManager.data_obj.__setattr__(attr, new_model.__getattribute__(attr))
                write_plugin_data(ConfigManager.data_obj) # 同步配置
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
