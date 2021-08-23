import platform
import miuitask
from urllib.request import getproxies


def show_info(tip, info):
    return "{}: {}".format(tip, info)


def system_info():
    miuitask.wLog(show_info("系统及版本信息", platform.platform()))
    miuitask.wLog(show_info('系统版本号', platform.version()))
    miuitask.wLog(show_info('系统名称', platform.system()))
    miuitask.wLog(show_info('系统位数', platform.architecture()))
    miuitask.wLog(show_info('计算机类型', platform.machine()))
    miuitask.wLog(show_info('处理器类型', platform.processor()))
    miuitask.wLog(show_info('Python版本', str(platform.python_version()) + ' ' + str(platform.python_build())))
    if getproxies():
        miuitask.wLog(show_info('系统代理', getproxies()))


if __name__ == '__main__':
    system_info()
