#!/usr/bin/python3
# -- coding: utf-8 --
#@Author : github@raindrop https://github.com/raindrop-hb/tencent-video
# @Time : 2023/3/31 10:23
# -------------------------------
# cron "30 0,1,2 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('腾讯视频签到');

import requests
import json
import time

push = '1' # 是否微信机器人推送，1为是，0为否，选择0则后面三项失效
corpid = 'ww7606bbf6c1cccea9'  # 企业ID
secret = 'CxY9TMEe-zsnUrGYXgS6au_hJpKJtUYd_kNiWBSh-X8'  # 应用的凭证密钥
agentid = '1000002' # 应用id

# 用列表存储多组账号参数
accounts = [
    {'vdevice_qimei36': '7a36822f71c2956c8b735159100016016509',
     'vqq_appid': '101483052',
     'vqq_openid': '94AE47E8F7B8E06C8CFF304ABE53F1D6',
     'vqq_access_token': 'CBA3921B82506FF382BC31F14AE9478A',
     'main_login': 'qq'},
    {'vdevice_qimei36': '7a36822f71c2956c8b735159100016016509',
     'vqq_appid': '101483052',
     'vqq_openid': '94AE47E8F7B8E06C8CFF304ABE53F1D6',
     'vqq_access_token': 'CBA3921B82506FF382BC31F14AE9478A',
     'main_login': 'qq'}
]

def ten_video(account):
    cookie = 'vdevice_qimei36=' + account['vdevice_qimei36'] + \
             ';vqq_appid=' + account['vqq_appid'] + \
             ';vqq_openid=' + account['vqq_openid'] + \
             ';vqq_access_token=' + account['vqq_access_token'] + \
             ';main_login=' + account['main_login']
             
    # 签到逻辑
    url_1 = 'https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/CheckIn?rpc_data=%7B%7D'
    headers_1 = {'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2104K10AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.7.85.27058',
                 'Content-Type': 'application/json',
                 'referer': 'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
                 'cookie': cookie}
    response_1 = requests.get(url_1, headers=headers_1)
    res_1 = json.loads(response_1.text)

    url_2 = 'https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/ProvideAward?rpc_data=%7B%22task_id%22:1%7D'
    headers_2 = {'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2104K10AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.7.85.27058',
                 'Content-Type': 'application/json',
                 'referer': 'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
                 'cookie': cookie}
    response_2 = requests.get(url_2, headers=headers_2)
    res_2 = json.loads(response_2.text)

    time_1 = int(time.time())
    time_2 = time.localtime(time_1)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time_2)
    log = "腾讯视频会员签到执行任务\n----------raindrop----------\n" + now

    try:
        log = log + "\n签到获得v力值:" + str(res_1['check_in_score'])
    except:
        log = log + "\n腾讯视频签到异常，返回内容：" + str(res_1)
        print(res_1)

    try:
        log = log + "\n观看获得v力值:" + str(res_2['check_in_score'])
    except:
        log = log + "\n腾讯视频领取观看积分异常，返回内容：" + str(res_2)
        print(res_2)

    url = 'https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/ReadTaskList?rpc_data=%7B%22business_id%22:%221%22,%22platform%22:3%7D'
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2104K10AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.7.85.27058',
               'Content-Type': 'application/json',
               'referer': 'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
               'cookie': cookie}
    response = requests.get(url, headers=headers)
    res = json.loads(response.text)

    try:
        lis = res["task_list"]
        log = log + '\n--------任务状态----------'
        for i in lis:
            log = log + '\n' + i["task_maintitle"] + '\n状态:' + i["task_subtitle"]
    except:
        log = log + "获取状态异常，可能是cookie失效"
        print(res)

    # 推送到企业微信
    print(push_a(log))


def push_a(content):
    if push == '0':
        print('不推送')
    else:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + secret
        access_token = requests.get(url)
        access_token = json.loads(access_token.text)
        access_token = access_token.get("access_token")

        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        data = json.dumps({
            "touser": "@all",
            "msgtype": "text",
            "agentid": agentid,
            "text": {
                "content": content
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        })
        resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
        return (json.loads(resp.text).get('errmsg'))


def main():
    for account in accounts:
        ten_video(account)


def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()
