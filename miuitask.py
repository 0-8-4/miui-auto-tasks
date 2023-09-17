# -- coding:UTF-8 --
import re
import requests
import time
import json
import hashlib

from urllib import request
from http import cookiejar
from typing import Any, Tuple

from utils.utils import system_info, get_config, w_log, s_log, check_config, format_config, random_sleep, \
    sleep_ten_sec_more, notify_me


class MIUITask:

    def __init__(self, uid, password, user_agent, device_id):
        self.uid = uid
        self.password = password
        self.user_agent = user_agent
        self.device_id = device_id

        # 留空
        self.cookie = ''
        # 留空
        self.miui_vip_ph = ''

    # 签名
    def post_sign(self, data):
        s_data = []
        for d in data:
            s_data.append(str(d) + '=' + str(data[d]))
        s_str = '&'.join(s_data)
        w_log('签名原文：' + str(s_str))
        s_str = hashlib.md5(str(s_str).encode(encoding='UTF-8')).hexdigest() + '067f0q5wds4'
        s_sign = hashlib.md5(str(s_str).encode(encoding='UTF-8')).hexdigest()
        w_log('签名结果：' + str(s_sign))
        return s_sign, data['timestamp']

    # 点赞
    def thumb_up(self):
        headers = {
            'cookie': str(self.cookie)
        }
        sign_data = {
            'postId': '36625780',
            'timestamp': int(round(time.time() * 1000))
        }
        sign = self.post_sign(sign_data)
        data = {
            'postId': '36625780',
            'sign': sign[0],
            'timestamp': sign[1]
        }
        try:
            response = requests.get('https://api.vip.miui.com/mtop/planet/vip/content/announceThumbUp', headers=headers,params=data)
            r_json = response.json()
            if r_json['code'] == 401:
                return w_log("点赞失败：Cookie无效")
            elif r_json['code'] != 200:
                return w_log("点赞失败：" + str(r_json['message']))
            w_log("点赞成功")
        except Exception as e:
            w_log("点赞出错")
            w_log(e)

    # 取消点赞
    def cancel_thumb_up(self):
        headers = {
            'cookie': str(self.cookie)
        }
        data = {
            'postId': '36625780'
        }
        try:
            response = requests.get('https://api.vip.miui.com/mtop/planet/vip/content/announceCancelThumbUp', headers=headers,params=data)
            r_json = response.json()
            if r_json['code'] == 401:
                return w_log("取消点赞失败：Cookie无效")
            elif r_json['code'] != 200:
                return w_log("取消点赞失败：" + str(r_json['message']))
            w_log("取消点赞成功")
        except Exception as e:
            w_log("取消点赞出错")
            w_log(e)

    def get_vip_cookie(self, url):

        try:
            r_cookie = cookiejar.CookieJar()
            handler = request.HTTPCookieProcessor(r_cookie)
            opener = request.build_opener(handler)
            response = opener.open(url)
            for item in r_cookie:
                self.cookie += item.name + '=' + item.value + ';'
            if self.cookie == '':
                return False
            ck_list = self.cookie.replace(" ", "").split(';')
            for ph in ck_list:
                if "miui_vip_ph=" in ph:
                    self.miui_vip_ph = ph.replace("miui_vip_ph=", "")
                    break
            return True
        except Exception as e:
            w_log(e)
            return False

    # 浏览帖子10s
    def browse_post(self):
        headers = {
            'cookie': str(self.cookie)
        }
        params = {
            'userId': str(self.uid),
            'action': 'BROWSE_POST_10S',
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.get('https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction',
                                    params=params, headers=headers)
            r_json = response.json()
            if r_json['status'] == 401:
                return w_log("浏览帖子失败：Cookie无效")
            elif r_json['status'] != 200:
                return w_log("浏览帖子完成，但有错误：" + str(r_json['message']))
            score = r_json['entity']['score']
            w_log("浏览帖子完成，成长值+" + str(score))
        except Exception as e:
            w_log("浏览帖子出错")
            w_log(e)

    # 浏览个人主页10s
    def browse_user_page(self):
        headers = {
            'cookie': str(self.cookie)
        }
        params = {
            'userId': str(self.uid),
            'action': 'BROWSE_SPECIAL_PAGES_USER_HOME',
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.get('https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction',
                                    params=params, headers=headers)
            r_json = response.json()
            if r_json['status'] == 401:
                return w_log("浏览个人主页失败：Cookie无效")
            elif r_json['status'] != 200:
                return w_log("浏览个人主页完成，但有错误：" + str(r_json['message']))
            score = r_json['entity']['score']
            w_log("浏览个人主页完成，成长值+" + str(score))
        except Exception as e:
            w_log("浏览个人主页出错")
            w_log(e)

    # 浏览指定专题页
    def browse_specialpage(self):
        headers = {
            'cookie': str(self.cookie)
        }
        params = {
            'userId': str(self.uid),
            'action': 'BROWSE_SPECIAL_PAGES_SPECIAL_PAGE',
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.get('https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction', 
                                    params=params, headers=headers)
            r_json = response.json()
            if r_json['status'] == 401:
                return w_log("浏览专题页失败：Cookie无效")
            elif r_json['status'] != 200:
                return w_log("浏览专题页完成，但有错误：" + str(r_json['message']))
            score = r_json['entity']['score']
            w_log("浏览专题页完成，成长值+" + str(score))
        except Exception as e:
            w_log("浏览专题页出错")
            w_log(e)

    # 加入小米圈子
    def board_follow(self):
        headers = {
            'cookie': str(self.cookie)
        }
        params = {
            'boardId': '558495',
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.post(
                'https://api.vip.miui.com/api/community/board/follow?'
                '&pathname=/mio/allboard&version=dev.20051',
                headers=headers,params=params)
            r_json = response.json()
            if r_json['status'] == 401:
                return w_log("加入小米圈子失败：Cookie无效")
            elif r_json['status'] != 200:
                return w_log("加入小米圈子失败：" + str(r_json['message']))
            w_log("加入小米圈子结果：" + str(r_json['message']))
        except Exception as e:
            w_log("加入小米圈子出错")
            w_log(e)

    # 退出小米圈子
    def board_unfollow(self):
        headers = {
            'cookie': str(self.cookie)
        }
        params = {
            'boardId': '558495',
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.post('https://api.vip.miui.com/api/community/board/unfollow?'
                                    '&pathname=/mio/allboard&version=dev.20051', headers=headers,params=params)
            r_json = response.json()
            if r_json['status'] == 401:
                return w_log("退出小米圈子失败：Cookie无效")
            elif r_json['status'] != 200:
                return w_log("退出小米圈子失败：" + str(r_json['message']))
            w_log("退出小米圈子结果：" + str(r_json['message']))
        except Exception as e:
            w_log("退出小米圈子出错")
            w_log(e)

    # 社区拔萝卜
    def carrot_pull(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'cookie': str(self.cookie)
        }
        data = {
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.post('https://api.vip.miui.com/api/carrot/pull', headers=headers,
                                     data=data)
            r_json = response.json()
            if r_json['code'] == 401:
                return w_log("社区拔萝卜失败：Cookie无效")
            elif r_json['code'] != 200:
                return w_log("社区拔萝卜失败：" + str(r_json['entity']['message']))
            w_log("社区拔萝卜结果：" + str(r_json['entity']['message']))
            money_count = r_json['entity']['header']['moneyCount']
            w_log("当前金币数：" + str(money_count))
        except Exception as e:
            w_log("社区拔萝卜出错")
            w_log(e)

    # 每日签到
    def check_in(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'cookie': str(self.cookie)
        }
        params = {
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.get(
                'https://api.vip.miui.com/mtop/planet/vip/user/checkin?pathname=/mio/checkIn&version=dev.1144',
                headers=headers,params=params)
            r_json = response.json()
            if r_json['status'] == 401:
                return w_log("每日签到失败：Cookie无效")
            elif r_json['status'] != 200:
                return w_log("每日签到失败：" + str(r_json['message']))
            w_log("每日签到结果：成长值+" + str(r_json['entity']))
        except Exception as e:
            w_log("每日签到出错")
            w_log(e)

    # 登录社区
    def login_app(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'cookie': str(self.cookie)
        }
        params = {
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.get('https://api.vip.miui.com/mtop/planet/vip/app/init/start/infos', headers=headers,params=params)
            r_code = response.status_code
            if r_code == 401:
                return w_log("登录社区失败：Cookie无效")
            elif r_code != 200:
                return w_log("登录社区失败")
            w_log("登录社区成功")
        except Exception as e:
            w_log("登录社区出错")
            w_log(e)

    def mi_login(self):
        proxies = {
            'https': None,
            'http': None
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://account.xiaomi.com/fe/service/login/password?sid=miui_vip&qs=%253Fcallback%253Dhttp'
                       '%25253A%25252F%25252Fapi.vip.miui.com%25252Fsts%25253Fsign%25253D4II4ABwZkiJzkd2YSkyEZukI4Ak'
                       '%2525253D%252526followup%25253Dhttps%2525253A%2525252F%2525252Fapi.vip.miui.com%2525252Fpage'
                       '%2525252Flogin%2525253FdestUrl%2525253Dhttps%252525253A%252525252F%252525252Fweb.vip.miui.com'
                       '%252525252Fpage%252525252Finfo%252525252Fmio%252525252Fmio%252525252FinternalTest%252525253Fref'
                       '%252525253Dhomepage%2526sid%253Dmiui_vip&callback=http%3A%2F%2Fapi.vip.miui.com%2Fsts%3Fsign'
                       '%3D4II4ABwZkiJzkd2YSkyEZukI4Ak%253D%26followup%3Dhttps%253A%252F%252Fapi.vip.miui.com%252Fpage'
                       '%252Flogin%253FdestUrl%253Dhttps%25253A%25252F%25252Fweb.vip.miui.com%25252Fpage%25252Finfo'
                       '%25252Fmio%25252Fmio%25252FinternalTest%25253Fref%25253Dhomepage&_sign=L%2BdSQY6sjSQ%2FCRjJs4p'
                       '%2BU1vNYLY%3D&serviceParam=%7B%22checkSafePhone%22%3Afalse%2C%22checkSafeAddress%22%3Afalse%2C'
                       '%22lsrp_score%22%3A0.0%7D&showActiveX=false&theme=&needTheme=false&bizDeviceType=',
            'User-Agent': str(self.user_agent),
            'Origin': 'https://account.xiaomi.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'deviceId=' + str(self.device_id) + '; pass_ua=web; uLocale=zh_CN'
        }
        data = {
            'bizDeviceType': '',
            'needTheme': 'false',
            'theme': '',
            'showActiveX': 'false',
            'serviceParam': '{"checkSafePhone":false,"checkSafeAddress":false,"lsrp_score":0.0}',
            'callback': 'http://api.vip.miui.com/sts?sign=4II4ABwZkiJzkd2YSkyEZukI4Ak%3D&followup=https%3A%2F%2Fapi.vip'
                        '.miui.com%2Fpage%2Flogin%3FdestUrl%3Dhttps%253A%252F%252Fweb.vip.miui.com%252Fpage%252Finfo'
                        '%252Fmio%252Fmio%252FinternalTest%253Fref%253Dhomepage',
            'qs': '%3Fcallback%3Dhttp%253A%252F%252Fapi.vip.miui.com%252Fsts%253Fsign%253D4II4ABwZkiJzkd2YSkyEZukI4Ak'
                  '%25253D%2526followup%253Dhttps%25253A%25252F%25252Fapi.vip.miui.com%25252Fpage%25252Flogin'
                  '%25253FdestUrl%25253Dhttps%2525253A%2525252F%2525252Fweb.vip.miui.com%2525252Fpage%2525252Finfo'
                  '%2525252Fmio%2525252Fmio%2525252FinternalTest%2525253Fref%2525253Dhomepage%26sid%3Dmiui_vip',
            'sid': 'miui_vip',
            '_sign': 'L+dSQY6sjSQ/CRjJs4p+U1vNYLY=',
            'user': str(self.uid),
            'cc': '+86',
            'hash': str(self.password),
            '_json': 'true'
        }
        try:
            response = requests.post('https://account.xiaomi.com/pass/serviceLoginAuth2', headers=headers, data=data,
                                     proxies=proxies)
            response_data = response.text.lstrip('&').lstrip('START').lstrip('&')
            r_json = json.loads(response_data)
            if r_json['code'] == 70016:
                w_log('小米账号登录失败：用户名或密码不正确')
                return False
            if r_json['code'] != 0:
                w_log('小米账号登录失败：' + r_json['desc'])
                return False
            if r_json['pwd'] != 1:
                w_log('当前账号需要短信验证码，请尝试修改UA或设备ID')
                return False
            if not self.get_vip_cookie(r_json['location']):
                w_log('小米账号登录成功，社区获取 Cookie 失败')
                return False
            w_log('账号登录完成')
            return True
        except Exception as e:
            w_log("登录小米账号出错")
            w_log(e)
            return False

    def check_daily_tasks(self):
        headers = {
        'cookie': str(self.cookie)
        }
        try:
            response = requests.get('https://api.vip.miui.com/mtop/planet/vip/member/getCheckinPageCakeList', headers=headers)
            r_json = response.json()
            if r_json['status'] != 200:
                w_log("获取每日任务状态失败：" + str(r_json['message']))
                return None

            tasks = r_json['entity']
            task_status = {}
            for task in tasks:
                if task['head']['title'] == "每日任务":
                    for daily_task in task['data']:
                        task_status[daily_task['title']] = daily_task['showType']
                        task_name = daily_task['title']
                        task_completion_status = "完成" if daily_task['showType'] == 0 else "未完成"
                        w_log("获取到信息: " + str(task_name) + ", " + str(task_completion_status))

            return task_status

        except Exception as e:
            w_log("获取信息出错")
            w_log(e)
            return None

    def get_point(self) -> Tuple[Any, Any]:
        """
        这个方法带返回值的原因是，可以调用这个方法获取返回值，可根据这个方法定制自己的“消息提示功能”。
        如：Qmsg发送到QQ 或者 发送邮件提醒
        :return: 当前的成长值
        """
        headers = {
            'cookie': str(self.cookie)
        }
        params = {
            'userId': str(self.uid),
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.get('https://api.vip.miui.com/mtop/planet/vip/member/getGrowUpPageData', headers=headers, params=params)
            r_json = response.json()
        
            your_point = re.findall(r"'title': '成长值'.*'title': '(\d+)'.*'title': '/'", str(r_json['entity']))[0]
            your_level = re.findall(r"'title': '(\d+段)', 'desc': '当前等级'", str(r_json['entity']))[0]
        
            w_log('当前等级：' + str(your_level) + ', 当前成长值：' + str(your_point))
        
            return your_point, your_level
        except Exception as e:
            w_log('成长值和等级获取失败')
            w_log(e)
            process_exception(e)


def process_exception(e: Exception):
    """
    全局异常处理
    :param e: 异常实例
    :return: No return
    """
    if e.__str__() == 'check_hostname requires server_hostname':
        w_log('系统设置了代理，出现异常')


def start(miui_task: MIUITask, check_in: bool, browse_post: bool, browse_user_page: bool, thumb_up: bool, browse_specialpage: bool, board_follow: bool, carrot_pull: bool):
    if miui_task.mi_login():
        w_log("本脚本用于模拟网络请求测试，仅供测试学习使用，禁止用于其他用途")
        w_log("本脚本默认不做任何操作，如您愿意承担一切可能的后果，可编辑配置文件手动打开需要的功能")
        w_log("为避免重复模拟请求，脚本将自动获取状态并决定是否继续模拟网络请求")
        miui_task.login_app()
        task_status = miui_task.check_daily_tasks()
        if task_status is None:
            w_log("无法获取状态，将跳过多数模拟请求功能")
        else:
            if "每日签到" in task_status and task_status.get("每日签到", 1) == 1 and check_in:
                w_log("模拟请求「每日签到」")
                random_sleep()
                miui_task.check_in()
            else:
                w_log("自动跳过模拟请求「每日签到」")

            if "浏览帖子超过10秒" in task_status and task_status.get("浏览帖子超过10秒", 1) == 1 and browse_post:
                w_log("模拟请求「浏览帖子超过10秒」")
                sleep_ten_sec_more()
                miui_task.browse_post()
            else:
                w_log("自动跳过模拟请求「浏览帖子超过10秒」")

            if "浏览个人/他人主页超过10秒" in task_status and task_status.get("浏览个人/他人主页超过10秒", 1) == 1 and browse_user_page:
                w_log("模拟请求「浏览个人/他人主页超过10秒」")
                sleep_ten_sec_more()
                miui_task.browse_user_page()
            else:
                w_log("自动跳过模拟请求「浏览个人/他人主页超过10秒」")

            if "点赞他人帖子" in task_status and task_status.get("点赞他人帖子", 1) == 1 and thumb_up:
                w_log("模拟请求「点赞他人帖子」")
                random_sleep()
                miui_task.thumb_up()
                random_sleep()
                miui_task.cancel_thumb_up()
            else:
                w_log("自动跳过模拟请求「点赞他人帖子」")

            if "浏览指定专题页" in task_status and task_status.get("浏览指定专题页", 1) == 1 and browse_specialpage:
                w_log("模拟请求「浏览指定专题页」")
                sleep_ten_sec_more()
                miui_task.browse_specialpage()
            else:
                w_log("自动跳过模拟请求「浏览指定专题页」")

            if "加入小米社区圈子" in task_status and task_status.get("加入小米社区圈子", 1) == 1 and board_follow:
                w_log("模拟请求「加入小米社区圈子」")
                random_sleep()
                miui_task.board_follow()
                random_sleep()
                miui_task.board_unfollow()
            else:
                w_log("自动跳过模拟请求「加入小米社区圈子」")
        w_log("请注意，未在配置文件启用或不需要执行的功能请求将被自动跳过，且不会支持“灌水”的功能")
        if carrot_pull:
            w_log("模拟请求「社区拔萝卜」")
            random_sleep()
            miui_task.carrot_pull()
        random_sleep()
        miui_task.get_point()


def main():
    w_log("MIUI-AUTO-TASK v1.6.0.1")
    w_log('---------- 系统信息 -------------')
    system_info()
    w_log('---------- 项目信息 -------------')
    w_log("这是一个免费且开源的项目，如果你是付费购买获得请务必退款")
    w_log("项目地址：https://github.com/0-8-4/miui-auto-tasks")
    w_log("欢迎 star，感谢東雲研究所中的大佬")
    w_log('---------- 配置检测 -------------')

    config = get_config()

    if not check_config(config):
        w_log('配置文件没有正确配置')
        exit(1)
    else:
        config = format_config(config)
        
    for i in config.get('accounts'):
        w_log('---------- EXECUTING -------------')
        start(
            MIUITask(i.get('uid'), i.get('password'), i.get('user-agent'), device_id=i.get('device-id')),
            i.get('check-in'), i.get('browse-post'), i.get('browse-user-page'), i.get('thumb-up'), i.get('browse-specialpage'), i.get('board-follow'), i.get('carrot-pull')
        )
        time.sleep(5)
    s_log(config.get('logging'))
    notify_me()


def main_handler(event, context):
    main()


if __name__ == "__main__":
    main()
