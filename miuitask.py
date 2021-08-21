# -- coding:UTF-8 --
import requests
import time
import json

from urllib import request
from http import cookiejar

# 小米ID
mid = ''
# 小米账号的密码MD5值，请使用"passwd2md5.py"转换
pMd5 = ''
# 避免登录失败，如果上面的md5中有小写字母，转换为大写
pMd5 = pMd5.upper()
# 如果登录一直需要短信验证码，在此填入设备id（在account.xiaomi.com的cookie中寻找deviceId）
devId = ''
# 常用浏览器UA
# 需要改成你自己常用的浏览器的UA
lUa = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
# 开发版内测5428803 开发版公测5433318 稳定版内测5462204 目前测试三个中完成任意一个即可全部完成
boardId = '5428803'
# 留空
cookie = ''
# 留空
miui_vip_ph = ''


def wLog(text):
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    print(now_localtime + ' | ' + str(text))


def thumbUp():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/post/thumbUp?postId=28270729', headers=headers)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("点赞失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("点赞失败：" + str(rJson['message']))
        wLog("点赞成功")
    except:
        wLog("点赞出错")


def cancelThumbUp():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/post/cancelThumbUp?postId=28270729',
                                headers=headers)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("取消点赞失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("取消点赞失败：" + str(rJson['message']))
        wLog("取消点赞成功")
    except:
        wLog("取消点赞出错")


def deletePost(tid):
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/post/detail/delete?postId=' + str(tid),
                                headers=headers)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("删除内容失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("删除内容失败：" + str(rJson['message']))
        wLog("删除内容成功：" + str(rJson['message']))
    except:
        wLog("删除内容出错，请手动删除")


# 发帖
def newAnnounce(tType):
    headers = {
        'cookie': str(cookie)
    }
    data = {
        'announce': '{"textContent":"小米社区闪退","boards":[{"boardId":"' + boardId + '"}],"announceType":"' + str(
            tType) + '"}',
        'miui_vip_ph': str(miui_vip_ph)
    }
    try:
        response = requests.post('https://api.vip.miui.com/api/community/post/add/newAnnounce', headers=headers,
                                 data=data)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("发表内容失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("发表内容失败：" + str(rJson['message']))
        postEntity = json.loads(rJson['entity'])
        wLog("发表内容成功，帖子ID：" + str(postEntity['announceId']) + "，将在3秒后删除")
        addCommentReturnCommentInfo(str(postEntity['announceId']))
        time.sleep(3)
        # 执行5次删帖是为了防止删帖失败
        for i in range(0, 5):
            deletePost(postEntity['announceId'])
    except:
        wLog("发表内容出错")


# 回帖
def addCommentReturnCommentInfo(tid):
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
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("回复失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("回复失败：" + str(rJson['message']))
        wLog("回复成功")
    except:
        wLog("回复出错")


def getVipCookie(url):
    global cookie
    global miui_vip_ph
    try:
        rCookie = cookiejar.CookieJar()
        handler = request.HTTPCookieProcessor(rCookie)
        opener = request.build_opener(handler)
        response = opener.open(url)
        for item in rCookie:
            cookie += item.name + '=' + item.value + ';'
        if cookie == '':
            return False
        cklist = cookie.replace(" ", "").split(';')
        for ph in cklist:
            if "miui_vip_ph=" in ph:
                miui_vip_ph = ph.replace("miui_vip_ph=", "")
                break
        return True
    except:
        return False


# 提交满意度问卷
def submitSurvey(sid):
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
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("满意度投票失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("满意度投票失败：" + str(rJson['message']))
        wLog("满意度投票成功")
    except:
        wLog("满意度投票出错")


# 获取满意度投票问卷ID
def getSurveyId():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/miui/dev/survey?businessId=2', headers=headers)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("获取问卷ID失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("获取问卷ID失败：" + str(rJson['message']))
        elif rJson['entity']['surveyInfo']['surveyId'] is None:
            wLog("获取问卷ID失败：问卷ID为空")
        surveyId = rJson['entity']['surveyInfo']['surveyId']
        wLog("获取问卷ID成功：" + str(surveyId))
        submitSurvey(surveyId)
    except:
        wLog("获取问卷ID出错，满意度投票失败")


# 取关用户
def unfollowUser():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/user/relation/unfollow?followeeId=210836962',
                                headers=headers)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("取关用户失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("取关用户失败：" + str(rJson['message']))
        wLog("取关用户成功")
    except:
        wLog("取关用户出错")


# 关注用户
def followUser():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/user/relation/follow?followeeId=210836962',
                                headers=headers)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("关注用户失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("关注用户失败：" + str(rJson['message']))
        wLog("关注用户成功")
    except:
        wLog("关注用户出错")


# 退出圈子
def unfollowBoard():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/board/unfollow?boardId=5462662',
                                headers=headers)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("退出圈子失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("退出圈子失败：" + str(rJson['message']))
        wLog("退出圈子成功")
    except:
        wLog("退出圈子出错")


# 加入圈子
def followBoard():
    headers = {
        'cookie': str(cookie)
    }
    try:
        response = requests.get('https://api.vip.miui.com/api/community/board/follow?boardId=5462662', headers=headers)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("加入圈子失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("加入圈子失败：" + str(rJson['message']))
        wLog("加入圈子成功")
    except:
        wLog("加入圈子出错")


# 活跃度任务领取
def startTask(taskId):
    headers = {
        'cookie': str(cookie)
    }
    data = {
        'taskId': str(taskId),
        'miui_vip_ph': str(miui_vip_ph)
    }
    try:
        response = requests.post('https://api.vip.miui.com/api/community/user/task/start?version=dev.210805',
                                 headers=headers, data=data)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("开始活跃分任务失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("开始活跃分任务失败：" + str(rJson['message']))
        wLog("开始活跃分任务成功")
    except:
        wLog("开始活跃分任务出错")


# 活跃度任务完成
def acquireTask(taskId):
    headers = {
        'cookie': str(cookie)
    }
    data = {
        'taskId': str(taskId),
        'miui_vip_ph': str(miui_vip_ph)
    }
    try:
        response = requests.post('https://api.vip.miui.com/api/community/user/task/acquire?version=dev.210805',
                                 headers=headers, data=data)
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("领取活跃分失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("领取活跃分失败：" + str(rJson['message']))
        wLog("领取活跃分成功")
    except:
        wLog("领取活跃分出错")

# 社区拔萝卜签到
def vipsignin():
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
        rJson = response.json()
        if rJson['code'] == 401:
            return wLog("社区拔萝卜签到失败：Cookie无效")
        elif rJson['code'] != 200:
            return wLog("社区拔萝卜签到失败：" + str(rJson['message']))
        wLog("社区拔萝卜签到成功")
    except:
        wLog("社区拔萝卜签到出错")


def milogin():
    proxies = {
        'https': None,
        'http': None
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://account.xiaomi.com/fe/service/login/password?sid=miui_vip&qs=%253Fcallback%253Dhttp%25253A%25252F%25252Fapi.vip.miui.com%25252Fsts%25253Fsign%25253D4II4ABwZkiJzkd2YSkyEZukI4Ak%2525253D%252526followup%25253Dhttps%2525253A%2525252F%2525252Fapi.vip.miui.com%2525252Fpage%2525252Flogin%2525253FdestUrl%2525253Dhttps%252525253A%252525252F%252525252Fweb.vip.miui.com%252525252Fpage%252525252Finfo%252525252Fmio%252525252Fmio%252525252FinternalTest%252525253Fref%252525253Dhomepage%2526sid%253Dmiui_vip&callback=http%3A%2F%2Fapi.vip.miui.com%2Fsts%3Fsign%3D4II4ABwZkiJzkd2YSkyEZukI4Ak%253D%26followup%3Dhttps%253A%252F%252Fapi.vip.miui.com%252Fpage%252Flogin%253FdestUrl%253Dhttps%25253A%25252F%25252Fweb.vip.miui.com%25252Fpage%25252Finfo%25252Fmio%25252Fmio%25252FinternalTest%25253Fref%25253Dhomepage&_sign=L%2BdSQY6sjSQ%2FCRjJs4p%2BU1vNYLY%3D&serviceParam=%7B%22checkSafePhone%22%3Afalse%2C%22checkSafeAddress%22%3Afalse%2C%22lsrp_score%22%3A0.0%7D&showActiveX=false&theme=&needTheme=false&bizDeviceType=',
        'User-Agent': str(lUa),
        'Origin': 'https://account.xiaomi.com',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'deviceId=' + str(devId) + '; pass_ua=web; uLocale=zh_CN'
    }
    data = {
        'bizDeviceType': '',
        'needTheme': 'false',
        'theme': '',
        'showActiveX': 'false',
        'serviceParam': '{"checkSafePhone":false,"checkSafeAddress":false,"lsrp_score":0.0}',
        'callback': 'http://api.vip.miui.com/sts?sign=4II4ABwZkiJzkd2YSkyEZukI4Ak%3D&followup=https%3A%2F%2Fapi.vip.miui.com%2Fpage%2Flogin%3FdestUrl%3Dhttps%253A%252F%252Fweb.vip.miui.com%252Fpage%252Finfo%252Fmio%252Fmio%252FinternalTest%253Fref%253Dhomepage',
        'qs': '%3Fcallback%3Dhttp%253A%252F%252Fapi.vip.miui.com%252Fsts%253Fsign%253D4II4ABwZkiJzkd2YSkyEZukI4Ak%25253D%2526followup%253Dhttps%25253A%25252F%25252Fapi.vip.miui.com%25252Fpage%25252Flogin%25253FdestUrl%25253Dhttps%2525253A%2525252F%2525252Fweb.vip.miui.com%2525252Fpage%2525252Finfo%2525252Fmio%2525252Fmio%2525252FinternalTest%2525253Fref%2525253Dhomepage%26sid%3Dmiui_vip',
        'sid': 'miui_vip',
        '_sign': 'L+dSQY6sjSQ/CRjJs4p+U1vNYLY=',
        'user': str(mid),
        'cc': '+86',
        'hash': str(pMd5),
        '_json': 'true'
    }
    try:
        response = requests.post('https://account.xiaomi.com/pass/serviceLoginAuth2', headers=headers, data=data,
                                 proxies=proxies)
        response_data = response.text.lstrip('&').lstrip('START').lstrip('&')
        rJson = json.loads(response_data)
        if rJson['code'] == 70016:
            wLog('小米账号登录失败：用户名或密码不正确')
            return False
        if rJson['code'] != 0:
            wLog('小米账号登录失败：' + rJson['desc'])
            return False
        if rJson['pwd'] != 1:
            wLog('当前账号需要短信验证码，请尝试修改UA或设备ID')
            return False
        if not getVipCookie(rJson['location']):
            wLog('小米账号登录成功，社区获取 Cookie 失败')
            return False
        wLog('账号登录完成')
        return True
    except:
        wLog("登录小米账号出错")
        return False


if __name__ == "__main__":
    wLog("miuitask v1.2.1")
    wLog("项目地址：https://github.com/0-8-4/miui-auto-tasks")
    wLog("欢迎star，感谢東雲研究所中的大佬")
    wLog("开始登录小米账号")
    if milogin():
        wLog("本脚本支持社区签到，因该功能存在风险默认禁用")
        wLog("如您愿意承担一切可能的后果，可编辑脚本手动打开该功能")
        # wLog("风险功能提示：正在进行社区签到")
        # vipsignin()
        # 警告：根据小米社区规则，非正常渠道签到可能会导致账户封禁
        # 本脚本虽是模拟您的操作向社区发送请求，但仍不能保证绝对安全
        # 如果您愿意自行承担一切风险，删去Line396和397的“#”即可
        startTask("10106263")
        wLog("正在完成BUG反馈任务")
        newAnnounce("7")
        wLog("3秒后执行提建议任务")
        acquireTask("10106263")
        time.sleep(3)
        wLog("正在完成提建议任务")
        newAnnounce("6")
        wLog("正在完成满意度调查任务")
        getSurveyId()
        wLog("正在完成点赞任务")
        startTask("10106256")
        for i in range(0, 5):
            thumbUp()
            time.sleep(0.2)
            cancelThumbUp()
            time.sleep(0.2)
        acquireTask("10106256")
        wLog("正在完成活跃分_关注任务")
        startTask("10106261")
        unfollowUser()
        followUser()
        wLog("5秒后领取活跃分_关注任务")
        time.sleep(5)
        acquireTask("10106261")
        wLog("正在完成活跃分_加圈任务")
        startTask("10106262")
        unfollowBoard()
        followBoard()
        wLog("5秒后领取活跃分_加圈任务")
        time.sleep(5)
        acquireTask("10106262")
        wLog("正在完成活跃分_发帖任务")
        startTask("10106265")
        newAnnounce("5")
        wLog("5秒后领取活跃分_发帖任务")
        time.sleep(5)
        acquireTask("10106265")
