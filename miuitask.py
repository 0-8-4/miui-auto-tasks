# -- coding:UTF-8 --
import requests
import time
import json

from urllib import request
from http import cookiejar
from utils.utils import system_info, get_config, w_log, s_log, conf_check


# Config
config = get_config()
# 小米ID
mi_id = config.get('MI_ID')
# 小米账号的密码MD5值，请使用"passwd2md5.py"转换
p_md5 = config.get('MI_PASSWORD').upper()
# 如果登录一直需要短信验证码，在此填入设备id（在account.xiaomi.com的cookie中寻找deviceId）
dev_id = ''
# 常用浏览器UA
# 需要改成你自己常用的浏览器的UA
l_ua = config.get('USER_AGENT')
# 开发版内测5428803 开发版公测5433318 稳定版内测5462204 目前测试三个中完成任意一个即可全部完成
board_id = config.get('BOARD_ID')
# 留空
cookie = ''
# 留空
miui_vip_ph = ''


def thumb_up():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/post/thumbUp?postId=28270729', headers=headers)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("点赞失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("点赞失败：" + str(r_json['message']))
        w_log("点赞成功")
    except:
        w_log("点赞出错")


def cancel_thumb_up():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/post/cancelThumbUp?postId=28270729',
                                headers=headers)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("取消点赞失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("取消点赞失败：" + str(r_json['message']))
        w_log("取消点赞成功")
    except:
        w_log("取消点赞出错")


def delete_post(tid):
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/post/detail/delete?postId=' + str(tid),
                                headers=headers)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("删除内容失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("删除内容失败：" + str(r_json['message']))
        w_log("删除内容成功：" + str(r_json['message']))
    except:
        w_log("删除内容出错，请手动删除")


# 发帖
def new_announce(t_type):
    headers = {
        'cookie': str(cookie)
    }
    data = {
        'announce': '{"textContent":"小米社区闪退","boards":[{"boardId":"' + board_id + '"}],"announceType":"' + str(
            t_type) + '"}',
        'miui_vip_ph': str(miui_vip_ph)
    }
    try:
        response = requests.post('https://api.vip.miui.com/api/community/post/add/newAnnounce', headers=headers,
                                 data=data)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("发表内容失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("发表内容失败：" + str(r_json['message']))
        post_entity = json.loads(r_json['entity'])
        w_log("发表内容成功，帖子ID：" + str(post_entity['announceId']) + "，将在3秒后删除")
        add_comment_return_comment_info(str(post_entity['announceId']))
        time.sleep(3)
        # 执行5次删帖是为了防止删帖失败
        for item in range(0, 5):
            delete_post(post_entity['announceId'])
    except:
        w_log("发表内容出错")


# 回帖
def add_comment_return_comment_info(tid):
    headers = {
        'cookie': str(cookie)
    }
    data = {
        'postId': str(tid),
        'text': '小米社区闪退',
        'miui_vip_ph': str(miui_vip_ph)
    }
    try:
        response = requests.post('https://api.vip.miui.com/mtop/planet/vip/content/addCommentReturnCommentInfo',
                                 headers=headers, data=data)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("回复失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("回复失败：" + str(r_json['message']))
        w_log("回复成功")
    except:
        w_log("回复出错")


def get_vip_cookie(url):
    global cookie
    global miui_vip_ph
    try:
        r_cookie = cookiejar.CookieJar()
        handler = request.HTTPCookieProcessor(r_cookie)
        opener = request.build_opener(handler)
        response = opener.open(url)
        for item in r_cookie:
            cookie += item.name + '=' + item.value + ';'
        if cookie == '':
            return False
        ck_list = cookie.replace(" ", "").split(';')
        for ph in ck_list:
            if "miui_vip_ph=" in ph:
                miui_vip_ph = ph.replace("miui_vip_ph=", "")
                break
        return True
    except:
        return False


# 提交满意度问卷
def submit_survey(sid):
    headers = {
        'cookie': str(cookie)
    }
    data = {
        'survey': '{"surveyId":' + str(sid) + ',"answer":{"1":"A"}}',
        'businessId': '2',
        'miui_vip_ph': str(miui_vip_ph)
    }
    try:
        response = requests.post('https://api.vip.miui.com/api/miui/dev/survey/submit', headers=headers, data=data)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("满意度投票失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("满意度投票失败：" + str(r_json['message']))
        w_log("满意度投票成功")
    except:
        w_log("满意度投票出错")


# 获取满意度投票问卷ID
def get_survey_id():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/miui/dev/survey?businessId=2', headers=headers)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("获取问卷ID失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("获取问卷ID失败：" + str(r_json['message']))
        elif r_json['entity']['surveyInfo']['surveyId'] is None:
            w_log("获取问卷ID失败：问卷ID为空")
        survey_id = r_json['entity']['surveyInfo']['surveyId']
        w_log("获取问卷ID成功：" + str(survey_id))
        submit_survey(survey_id)
    except:
        w_log("获取问卷ID出错，满意度投票失败")


# 取关用户
def unfollow_user():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/user/relation/unfollow?followeeId=210836962',
                                headers=headers)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("取关用户失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("取关用户失败：" + str(r_json['message']))
        w_log("取关用户成功")
    except:
        w_log("取关用户出错")


# 关注用户
def follow_user():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/user/relation/follow?followeeId=210836962',
                                headers=headers)
        rJson = response.json()
        if rJson['code'] == 401:
            return w_log("关注用户失败：Cookie无效")
        elif rJson['code'] != 200:
            return w_log("关注用户失败：" + str(rJson['message']))
        w_log("关注用户成功")
    except:
        w_log("关注用户出错")


# 退出圈子
def unfollow_board():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/board/unfollow?boardId=5462662',
                                headers=headers)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("退出圈子失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("退出圈子失败：" + str(r_json['message']))
        w_log("退出圈子成功")
    except:
        w_log("退出圈子出错")


# 加入圈子
def follow_board():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/board/follow?boardId=5462662', headers=headers)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("加入圈子失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("加入圈子失败：" + str(r_json['message']))
        w_log("加入圈子成功")
    except:
        w_log("加入圈子出错")


# 活跃度任务领取
def start_task(task_id):
    headers = {
        'cookie': str(cookie)
    }
    data = {
        'taskId': str(task_id),
        'miui_vip_ph': str(miui_vip_ph)
    }
    try:
        response = requests.post('https://api.vip.miui.com/api/community/user/task/start?version=dev.210805',
                                 headers=headers, data=data)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("开始活跃分任务失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("开始活跃分任务失败：" + str(r_json['message']))
        w_log("开始活跃分任务成功")
    except:
        w_log("开始活跃分任务出错")


# 活跃度任务完成
def acquire_task(task_id):
    headers = {
        'cookie': str(cookie)
    }
    data = {
        'taskId': str(task_id),
        'miui_vip_ph': str(miui_vip_ph)
    }
    try:
        response = requests.post('https://api.vip.miui.com/api/community/user/task/acquire?version=dev.210805',
                                 headers=headers, data=data)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("领取活跃分失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("领取活跃分失败：" + str(r_json['message']))
        w_log("领取活跃分成功")
    except:
        w_log("领取活跃分出错")


# 社区拔萝卜签到
def vip_sign_in():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'cookie': str(cookie)
    }
    data = {
        'miui_vip_ph': str(miui_vip_ph)
    }
    try:
        response = requests.post('https://api.vip.miui.com/api/carrot/pull', headers=headers,
                                 data=data)
        r_json = response.json()
        if r_json['code'] == 401:
            return w_log("社区拔萝卜签到失败：Cookie无效")
        elif r_json['code'] != 200:
            return w_log("社区拔萝卜签到失败：" + str(r_json['message']))
        w_log("社区拔萝卜签到成功")
    except:
        w_log("社区拔萝卜签到出错")


def mi_login():
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
        'User-Agent': str(l_ua),
        'Origin': 'https://account.xiaomi.com',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'deviceId=' + str(dev_id) + '; pass_ua=web; uLocale=zh_CN'
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
        'user': str(mi_id),
        'cc': '+86',
        'hash': str(p_md5),
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
        if not get_vip_cookie(r_json['location']):
            w_log('小米账号登录成功，社区获取 Cookie 失败')
            return False
        w_log('账号登录完成')
        return True
    except:
        w_log("登录小米账号出错")
        return False


def get_score() -> int:
    """
    这个方法待返回值的原因是，可以调用这个方法获取返回值，可根据这个方法定制自己的“消息提示功能”。
    如：Qmsg发送到QQ 或者 发送邮件提醒
    :return: 当前的内测分值
    """
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/mtop/planet/vip/betaTest/score', headers=headers)
        r_json = response.json()
        your_score = r_json['entity']
        w_log('成功获取内测分,当前内测分：' + str(your_score))
        return your_score
    except Exception as e:
        w_log('内测分获取失败')
        process_exception(e)


def process_exception(e: Exception):
    """
    全局异常处理
    :param e: 异常实例
    :return: No return
    """
    if e.__str__() == 'check_hostname requires server_hostname':
        w_log('系统设置了代理，出现异常')


if __name__ == "__main__":
    w_log("MIUITask_v1.3")
    w_log('----------系统信息-开始-------------')
    system_info()
    w_log('----------系统信息-结束-------------')
    w_log("项目地址：https://github.com/0-8-4/miui-auto-tasks")
    w_log("欢迎star，感谢東雲研究所中的大佬")
    w_log('----------检测配置文件-------------')
    if conf_check(config):
        w_log('----------------------------------')
        w_log("开始登录小米账号")
        if mi_login():
            w_log("本脚本支持社区签到，因该功能存在风险默认禁用")
            w_log("如您愿意承担一切可能的后果，可编辑配置文件手动打开该功能")
            if config.get('SIGN_IN'):
                w_log("风社险功能提示：正在进行区签到")
                vip_sign_in()
            start_task("10106263")
            w_log("正在完成BUG反馈任务")
            new_announce("7")
            w_log("3秒后执行提建议任务")
            acquire_task("10106263")
            time.sleep(3)
            w_log("正在完成提建议任务")
            new_announce("6")
            w_log("正在完成满意度调查任务")
            get_survey_id()
            w_log("正在完成点赞任务")
            start_task("10106256")
            for i in range(0, 5):
                thumb_up()
                time.sleep(0.2)
                cancel_thumb_up()
                time.sleep(0.2)
            acquire_task("10106256")
            w_log("正在完成活跃分_关注任务")
            start_task("10106261")
            unfollow_user()
            follow_user()
            w_log("5秒后领取活跃分_关注任务")
            time.sleep(5)
            acquire_task("10106261")
            w_log("正在完成活跃分_加圈任务")
            start_task("10106262")
            unfollow_board()
            follow_board()
            w_log("5秒后领取活跃分_加圈任务")
            time.sleep(5)
            acquire_task("10106262")
            w_log("正在完成活跃分_发帖任务")
            start_task("10106265")
            new_announce("5")
            w_log("5秒后领取活跃分_发帖任务")
            time.sleep(5)
            acquire_task("10106265")
            get_score()
    s_log()
