import time
import platform

from hashlib import md5
from dotenv import dotenv_values
from urllib.request import getproxies


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
    config = dotenv_values(".env")
    passwd = config.get('MI_PASSWORD')
    if len(passwd) != 32:
        config['MI_PASSWORD'] = md5_crypto(passwd)
    if config.get('SIGN_IN').upper() in ('Y', 'YES'):
        config['SIGN_IN'] = True
    return config
    

def w_log(text):
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    print(now_localtime + ' | ' + str(text))


def conf_check(config: dict):
    if not config.get('MI_ID'):
        w_log('小米账户 ID 未配置')
        exit(127)
    if not config.get('MI_PASSWORD'):
        w_log('小米账户 密码 / MD5 未配置')
        exit(127)
    if not config.get('USER_AGENT'):
        w_log('User-Agent 未配置')
        exit(127)
    if not config.get('BOARD_ID'):
        w_log('测试类型 ID 未配置')
        exit(127)
    w_log('.env 已配置')


if __name__ == '__main__':
    print(get_config())
    # print(get_config()['MI_PASSWORD'])