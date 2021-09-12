import os
import time
import platform

from hashlib import md5

import dotenv
from dotenv import dotenv_values
from urllib.request import getproxies


logs = ''


def md5_crypto(passwd: str) -> str:
    return md5(passwd.encode('utf8')).hexdigest()


def show_info(tip, info):
    return "{}: {}".format(tip, info)


def system_info():
    w_log(show_info("系统及版本信息", platform.platform()))
    w_log(show_info('系统版本号', platform.version()))
    w_log(show_info('系统名称', platform.system()))
    w_log(show_info('系统位数', platform.architecture()))
    w_log(show_info('计算机类型', platform.machine()))
    w_log(show_info('处理器类型', platform.processor()))
    w_log(show_info('Python版本', str(platform.python_version()) + ' ' + str(platform.python_build())))
    if getproxies():
        w_log(show_info('系统代理', getproxies()))


def get_config() -> dict:
    w_log('正在使用' + dotenv.find_dotenv() + '配置文件')
    config_path = dotenv.find_dotenv()
    config = dotenv.dotenv_values(config_path)
    if not config:
        w_log('配置文件未配置，请编辑项目目录的.env文件。如文件不存在请自行创建')
        exit(1)
    passwd = config.get('MI_PASSWORD')
    if len(passwd) != 32:
        config['MI_PASSWORD'] = md5_crypto(passwd)
    if config.get('SIGN_IN').upper() in ('Y', 'YES'):
        config['SIGN_IN'] = True
    else:
        config['SIGN_IN'] = False
    return config
    

def w_log(text):
    global logs
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    logs += now_localtime + ' | ' + str(text) + '\n'
    print(now_localtime + ' | ' + str(text))


def s_log():
    logs_save= get_config().get('LOG_SAVE')
    if logs_save == 'Y':
        global logs
        folder = os.path.exists('./logs')
        if not folder:
            os.makedirs('./logs')
        now_localtime = time.strftime("%Y-%m-%d", time.localtime())
        fname = now_localtime + '.log'
        with open('./logs/' + fname, 'a+', encoding='utf-8') as f:
            f.write(logs)


def conf_check(config: dict):
    if not config.get('MI_ID'):
        w_log('小米账户 ID 未配置')
        return False
    if not config.get('MI_PASSWORD'):
        w_log('小米账户 密码 / MD5 未配置')
        return False
    if not config.get('USER_AGENT'):
        w_log('User-Agent 未配置')
        return False
    if not config.get('BOARD_ID'):
        w_log('测试类型 ID 未配置')
        return False
    w_log('config.env 已配置')
    return True
