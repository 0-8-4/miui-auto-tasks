import os
import time
import platform
import dotenv, yaml

from hashlib import md5
from urllib.request import getproxies


logs = ''


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
    config = {'account': []}
    config_path_legacy = dotenv.find_dotenv(filename='config.env')
    config_path_yaml = dotenv.find_dotenv(filename='config.yaml')

    if config_path_legacy:
        w_log('正在使用 ' + config_path_legacy + ' 作为配置文件')
        legacy_config = dotenv.dotenv_values(config_path_legacy)
        config['account'].append({'uid': legacy_config.get('MI_ID')})
        config['account'][0]['password'] = legacy_config.get('MI_PASSWORD')
        config['account'][0]['user-agent'] = legacy_config.get('USER_AGENT')
        config['account'][0]['board-id'] = legacy_config.get('BOARD_ID')
        if legacy_config.get('SIGN_IN') and legacy_config.get('SIGN_IN').upper() in ('Y', 'YES'):
            config['account'][0]['check-in'] = True
        else:
            config['account'][0]['check-in'] = False
        if legacy_config.get('ENHANCED_MODE') and legacy_config.get('ENHANCED_MODE').upper() in ('Y', 'YES'):
            config['account'][0]['enhance-mode'] = True
        else:
            config['account'][0]['enhance-mode'] = False
        if legacy_config.get('LOG_SAVE') and legacy_config.get('LOG_SAVE').upper() in ('Y', 'YES'):
            config['logging'] = True
        else:
            config['logging'] = False
        return config
    elif config_path_yaml:
        w_log('正在使用 ' + config_path_yaml + ' 作为配置文件')
        with open(config_path_yaml, "rb") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                w_log('配置文件载入错误')
                w_log(e)
            return config
    else:
        w_log('配置文件不存在')
        exit(1)


def w_log(text):
    global logs
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    logs += now_localtime + ' | ' + str(text) + '\n'
    print(now_localtime + ' | ' + str(text))


def s_log(flag):
    if flag == True:
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
            if not i.get('uid') or not i.get('password') or not i.get('user-agent') or not i.get('board-id'):
                return False
            if not isinstance(i.get('check-in'), bool) or not isinstance(i.get('enhance-mode'), bool):
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
        i['board-id'] = str(i.get('board-id'))
        if len(i.get('password')) != 32:
            i['password'] = md5_crypto(i.get('password')).upper()
        else:
            i['password'] = str(i.get('password')).upper()
        if i.get('device-id'):
            i['device-id'] = str(i.get('device-id'))
        else:
            i['device-id'] = None
    return config
