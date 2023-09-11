import os
import random
import time
import platform
import dotenv
import yaml

from hashlib import md5
from onepush import notify
from urllib.request import getproxies

logs = ''
message = ''
config = {'account': []}
CONFIG_VERSION_REQUIRE: str = 'v1.6.0'


def md5_crypto(passwd: str) -> str:
    return md5(passwd.encode('utf8')).hexdigest()


def show_info(tip, info):
    return "{}: {}".format(tip, info)


def system_info():
    w_log(show_info('操作系统平台', platform.platform()))
    w_log(show_info('操作系统版本', platform.version()))
    w_log(show_info('操作系统名称', platform.system()))
    w_log(show_info('操作系统位元', platform.architecture()))
    w_log(show_info('操作系统类型', platform.machine()))
    w_log(show_info('处理器信息', platform.processor()))
    w_log(show_info('Python 版本', str(platform.python_version()) + ' ' + str(platform.python_build())))
    if getproxies():
        w_log(show_info('系统代理', getproxies()))


def get_config() -> dict:
    global config
    config_path_legacy = dotenv.find_dotenv(filename='config.env')
    config_path_yaml = dotenv.find_dotenv(filename='config.yaml')

    # yaml config
    if config_path_yaml:
        w_log('正在加载 ' + config_path_yaml + ' 配置文件')
        with open(config_path_yaml, "rb") as stream:
            try:
                config = yaml.safe_load(stream)
                config_version: str = config.get('version')

                # check config file version
                # if config version not meet the requirement
                if CONFIG_VERSION_REQUIRE != config_version:
                    w_log('配置文件版本和程序运行要求版本不匹配，请检查配置文件')
                    w_log('配置文件版本: ' + config_version)
                    w_log('运行程序配置版本要求: ' + CONFIG_VERSION_REQUIRE)
                    exit(1)  # exit the program
                w_log('配置文件已成功加载，文件版本 ' + config_version)

            except yaml.YAMLError as e:
                w_log('配置文件载入错误')
                w_log(e)
            return config
    else:
        w_log('配置文件不存在')
        exit(1)


def w_log(text):
    global logs
    global message
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    logs += now_localtime + ' | ' + str(text) + '\n'
    message += str(text) + '\n'
    print(now_localtime + ' | ' + str(text))


def s_log(flag):
    if flag:
        global logs
        folder = os.path.exists('./logs')
        if not folder:
            os.makedirs('./logs')
        now_localtime = time.strftime("%Y-%m-%d", time.localtime())
        fname = now_localtime + '.log'
        with open('./logs/' + fname, 'a+', encoding='utf-8') as f:
            f.write(logs)


def check_config(config: dict) -> bool:
    if config.get('accounts'):
        for i in config.get('accounts'):
            if not i.get('uid') or not i.get('password') or not i.get('user-agent'):
                return False
            if not isinstance(i.get('check-in'), bool):
                return False
            if not isinstance(i.get('browse-user-page'), bool):
                return False
            if not isinstance(i.get('browse-post'), bool):
                return False
            if not isinstance(i.get('thumb-up'), bool):
                return False
            if not isinstance(i.get('browse-specialpage'), bool):
                return False
            if not isinstance(i.get('board-follow'), bool):
                return False
            if not isinstance(i.get('carrot-pull'), bool):
                return False
    else:
        return False
    if not isinstance(config.get('logging'), bool):
        return False
    return True


def format_config(config: dict) -> dict:
    for i in config.get('accounts'):
        i['uid'] = str(i.get('uid'))
        i['user-agent'] = str(i.get('user-agent'))
        if len(i.get('password')) != 32:
            i['password'] = md5_crypto(i.get('password')).upper()
        else:
            i['password'] = str(i.get('password')).upper()
        if i.get('device-id'):
            i['device-id'] = str(i.get('device-id'))
        else:
            i['device-id'] = None
    return config


def random_sleep():
    time.sleep(random.randint(1, 9))


def sleep_ten_sec_more():
    time.sleep(random.randint(10, 12))


def notify_me(content=None):
    """
    默认推送日志
    """
    global message
    global config
    if not content:
        content = message
    notifier = config.get('ONEPUSH', {}).get('notifier', '')
    params = config.get('ONEPUSH', {}).get('params', '')
    if not notifier or not params:
        s_log('未配置推送或未正确配置推送')
        return
    if not config.get('ONEPUSH', {}).get('title', ''):
        config['ONEPUSH']['title'] = ''
    return notify(notifier, content=content, **params)
