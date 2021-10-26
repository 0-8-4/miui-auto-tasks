# -- coding:UTF-8 --
import requests
import time
import json
import hashlib

from urllib import request
from http import cookiejar
from utils.utils import system_info, get_config, w_log, s_log, conf_check


class MIUITask:

    def __init__(self, mi_id, p_md5, l_ua, board_id, dev_id=None):
        self.mi_id = mi_id
        self.p_md5 = p_md5
        self.l_ua = l_ua
        self.board_id = board_id

        if not dev_id:
            self.dev_id = dev_id

        # 留空
        self.cookie = ''
        # 留空
        self.miui_vip_ph = ''

    def thumb_up(self):
        headers = {
            'cookie': str(self.cookie)
        }
        try:
            response = requests.get('https://api.vip.miui.com/api/community/post/thumbUp?postId=28270729',
                                    headers=headers)
            r_json = response.json()
            if r_json['code'] == 401:
                return w_log("点赞失败：Cookie无效")
            elif r_json['code'] != 200:
                return w_log("点赞失败：" + str(r_json['message']))
            w_log("点赞成功")
        except Exception as e:
            w_log("点赞出错")
            w_log(e)

    def cancel_thumb_up(self):
        headers = {
            'cookie': str(self.cookie)
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
        except Exception as e:
            w_log("取消点赞出错")
            w_log(e)

    def delete_post(self, tid):
        headers = {
            'cookie': str(self.cookie)
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
        except Exception as e:
            w_log("删除内容出错，请手动删除")
            w_log(e)
    
    # 发帖签名
    def post_sign(self,data):
        s_data = []
        for d in data:
            s_data.append(str(d) + '=' + str(data[d]))
        s_str = '&'.join(s_data)
        w_log('签名原文：' + str(s_str))
        s_str = hashlib.md5(str(s_str).encode(encoding='UTF-8')).hexdigest() + '067f0q5wds4'
        s_sign = hashlib.md5(str(s_str).encode(encoding='UTF-8')).hexdigest()
        w_log('签名结果：' + str(s_sign))
        return s_sign, data['timestamp']

    # 发帖
    def new_announce(self, t_type):
        headers = {
            'cookie': str(self.cookie)
        }
        sign_data = {
        'announce': '{"textContent":"小米社区白屏","boards":[{"boardId":"' + self.board_id + '"}],"announceType":"' + str(t_type) + '","extraStatus":1,"extraA":"","extraB":null}',
        'timestamp': int(round(time.time() * 1000))
        }
        sign = self.post_sign(sign_data)
        data = {
            'announce': sign_data['announce'],
            'pageType': '1',
            'miui_vip_ph': str(self.miui_vip_ph),
            'sign': sign[0],
            'timestamp': sign[1]
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
            self.add_comment_return_comment_info(str(post_entity['announceId']))
            time.sleep(3)
            # 执行5次删帖是为了防止删帖失败
            for item in range(0, 5):
                self.delete_post(post_entity['announceId'])
        except Exception as e:
            w_log("发表内容出错")
            w_log(e)

    # 回帖
    def add_comment_return_comment_info(self, tid):
        headers = {
            'cookie': str(self.cookie)
        }
        post_text = '小米社区白屏'
        sign_data = {
            'postId': str(tid),
            'text': post_text,
            'timestamp': int(round(time.time() * 1000))
        }
        sign = self.post_sign(sign_data)
        data = {
            'postId': str(tid),
            'text': post_text,
            'miui_vip_ph': str(self.miui_vip_ph),
            'sign': sign[0],
            'timestamp': sign[1]
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
        except Exception as e:
            w_log("回复出错")
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

    # 提交满意度问卷
    def submit_survey(self, sid):
        headers = {
            'cookie': str(self.cookie)
        }
        data = {
            'survey': '{"surveyId":' + str(sid) + ',"answer":{"1":"A"}}',
            'businessId': '2',
            'miui_vip_ph': str(self.miui_vip_ph)
        }
        try:
            response = requests.post('https://api.vip.miui.com/api/miui/dev/survey/submit', headers=headers, data=data)
            r_json = response.json()
            if r_json['code'] == 401:
                return w_log("满意度投票失败：Cookie无效")
            elif r_json['code'] != 200:
                return w_log("满意度投票失败：" + str(r_json['message']))
            w_log("满意度投票成功")
        except Exception as e:
            w_log("满意度投票出错")
            w_log(e)

# 获取满意度投票问卷ID
    def get_survey_id(self):
        headers = {
            'cookie': str(self.cookie)
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
            self.submit_survey(survey_id)
        except Exception as e:
            w_log("获取问卷ID出错，满意度投票失败")
            w_log(e)

    # 取关用户
    def unfollow_user(self):
        headers = {
            'cookie': str(self.cookie)
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
        except Exception as e:
            w_log("取关用户出错")
            w_log(e)

    # 关注用户
    def follow_user(self):
        headers = {
            'cookie': str(self.cookie)
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
        except Exception as e:
            w_log("关注用户出错")
            w_log(e)

    # 退出圈子
    def unfollow_board(self):
        headers = {
            'cookie': str(self.cookie)
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
        except Exception as e:
            w_log("退出圈子出错")
            w_log(e)

    # 加入圈子
    def follow_board(self):
        headers = {
            'cookie': str(self.cookie)
        }
        try:
            response = requests.get('https://api.vip.miui.com/api/community/board/follow?boardId=5462662', headers=headers)
            r_json = response.json()
            if r_json['code'] == 401:
                return w_log("加入圈子失败：Cookie无效")
            elif r_json['code'] != 200:
                return w_log("加入圈子失败：" + str(r_json['message']))
            w_log("加入圈子成功")
        except Exception as e:
            w_log("加入圈子出错")

    # 活跃度任务领取
    def start_task(self, task_id):
        headers = {
            'cookie': str(self.cookie)
        }
        data = {
            'taskId': str(task_id),
            'miui_vip_ph': str(self.miui_vip_ph)
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
        except Exception as e:
            w_log("开始活跃分任务出错")
            w_log(e)

    # 活跃度任务完成
    def acquire_task(self, task_id):
        headers = {
            'cookie': str(self.cookie)
        }
        data = {
            'taskId': str(task_id),
            'miui_vip_ph': str(self.miui_vip_ph)
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
        except Exception as e:
            w_log("领取活跃分出错")
            w_log(e)

    # 社区拔萝卜签到
    def vip_sign_in(self):
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
                return w_log("社区拔萝卜签到失败：Cookie无效")
            elif r_json['code'] != 200:
                return w_log("社区拔萝卜签到失败：" + str(r_json['message']))
            w_log("社区拔萝卜签到成功")
        except Exception as e:
            w_log("社区拔萝卜签到出错")
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
            'User-Agent': str(self.l_ua),
            'Origin': 'https://account.xiaomi.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'deviceId=' + str(self.dev_id) + '; pass_ua=web; uLocale=zh_CN'
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
            'user': str(self.mi_id),
            'cc': '+86',
            'hash': str(self.p_md5),
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

    def get_score(self) -> int:
        """
        这个方法待返回值的原因是，可以调用这个方法获取返回值，可根据这个方法定制自己的“消息提示功能”。
        如：Qmsg发送到QQ 或者 发送邮件提醒
        :return: 当前的内测分值
        """
        headers = {
            'cookie': str(self.cookie)
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


def start(miui_task: MIUITask, sign_in: bool, enhanced_mode: bool):

    if miui_task.mi_login():
        w_log("本脚本支持社区签到，因该功能存在风险默认禁用")
        w_log("如您愿意承担一切可能的后果，可编辑配置文件手动打开该功能")
        if sign_in:
            w_log("风险功能提示：正在进行社区签到")
            miui_task.vip_sign_in()
        w_log("正在完成满意度调查任务")
        miui_task.get_survey_id()
        w_log("正在完成点赞任务")
        miui_task.start_task("10106256")
        miui_task.thumb_up()
        time.sleep(0.2)
        miui_task.cancel_thumb_up()
        time.sleep(0.2)
        miui_task.acquire_task("10106256")
        w_log("正在完成活跃分_关注任务")
        miui_task.start_task("10106261")
        miui_task.unfollow_user()
        miui_task.follow_user()
        w_log("5秒后领取活跃分_关注任务")
        time.sleep(5)
        miui_task.acquire_task("10106261")
        w_log("正在完成活跃分_加圈任务")
        miui_task.start_task("10106262")
        miui_task.unfollow_board()
        miui_task.follow_board()
        w_log("5秒后领取活跃分_加圈任务")
        time.sleep(5)
        miui_task.acquire_task("10106262")
        if enhanced_mode:
            w_log("风险功能提示：增强模式已启用")
            w_log("增强模式已启用，存在封号风险")
            miui_task.start_task("10106263")
            w_log("正在完成BUG反馈任务")
            miui_task.new_announce("7")
            w_log("3秒后执行提建议任务")
            miui_task.acquire_task("10106263")
            time.sleep(3)
            w_log("正在完成提建议任务")
            miui_task.new_announce("6")
            w_log("正在完成活跃分_发帖任务")
            miui_task.start_task("10106265")
            miui_task.new_announce("3")
            w_log("5秒后领取活跃分_发帖任务")
            time.sleep(5)
            miui_task.acquire_task("10106265")
        miui_task.get_score()


def main():
    w_log("MIUITask_v1.3.3")
    w_log('----------系统信息-开始-------------')
    system_info()
    w_log('----------系统信息-结束-------------')
    w_log("项目地址：https://github.com/0-8-4/miui-auto-tasks")
    w_log("欢迎star，感谢東雲研究所中的大佬")
    w_log('----------检测配置文件-------------')

    config = get_config()
    if not conf_check(config):
        w_log('配置文件没有正确配置，请检查')

    mi_id = config.get('MI_ID')
    p_md5 = config.get('MI_PASSWORD').upper()
    l_ua = config.get('USER_AGENT')
    board_id = config.get('BOARD_ID')

    miui = MIUITask(mi_id, p_md5, l_ua, board_id)
    start(miui, config.get('SIGN_IN'), config.get('ENHANCED_MODE'))

    s_log()


if __name__ == "__main__":
    main()
