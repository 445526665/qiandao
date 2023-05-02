#!/usr/bin/python3
# -- coding: utf-8 --
#@Author : github https://github.com/445526665/qiandao
# @Time : 2023/3/31 10:23
# -------------------------------
# cron "30 0,1,2 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('腾讯视频签到');

import requests
import json
import time

push = '1' # 是否 Push Plus 推送，1为是，0为否
pp_token = 'f62e59644fac404cae0fea8df8f96d3d' # Push Plus 推送的 token
pp_topic = '腾讯视频签到' # Push Plus 推送的主题

wechat_push = '1' # 是否企业微信推送，1为是，0为否
corpid = 'ww7606bbf6c1cccea9' # 企业ID
secret = 'CxY9TMEe-zsnUrGYXgS6au_hJpKJtUYd_kNiWBSh-X8' # 应用的凭证密钥
agentid = '1000002' # 应用id

# 用列表存储多组账号参数
accounts = [
    {
        "QQ": "测试1",
        'vdevice_qimei36': '7a36822f71c2956c8b735159100016016509',
        'vqq_appid': '101483052',
        'vqq_openid': '94AE47E8F7B8E06C8CFF304ABE53F1D6',
        'vqq_access_token': 'CBA3921B82506FF382BC31F14AE9478A',
        'main_login': 'qq'
    },
    {
        "QQ": "663308887",
        'vdevice_qimei36': '7a36822f71c2956c8b735159100016016509',
        'vqq_appid': '101795054',
        'vqq_openid': '08EB8016AA6A6B08EDFF3ACEF00EAABF',
        'vqq_access_token': 'DFCF0D0D678C795B2C777B5E98168A3D',
        'main_login': 'qq'
    },
    {
        "QQ": "445526665",
        'vdevice_qimei36': '7a36822f71c2956c8b735159100016016509',
        'vqq_appid': '101795054',
        'vqq_openid': '43285A136DB930761BD5F661A1BD989E',
        'vqq_access_token': '8736F76727950AB41F2FE3BEF2BB20D0',
        'main_login': 'qq'
    }
]

def ten_video(account):
    cookie = 'vdevice_qimei36=' + account['vdevice_qimei36'] + \
             ';vqq_appid=' + account['vqq_appid'] + \
             ';vqq_openid=' + account['vqq_openid'] + \
             ';vqq_access_token=' + account['vqq_access_token'] + \
             ';main_login=' + account['main_login']
      # 签到
    time_1 = int(time.time())
    time_2 = time.localtime(time_1)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time_2)
    log = "腾讯视频会员签到执行任务\n" + now + '\nQQ:' + account['QQ']
    #积分查询
    url_3 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_vscore_user_mashup&cmd=&otype=xjson&type=1'
    headers_3 = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2104K10AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.7.85.27058',
        'Content-Type': 'application/json',
        'cookie': cookie
    }
    response_3 = requests.get(url_3, headers=headers_3)
    try:
        res_3 = json.loads(response_3.text)
        log = log + "\n会员等级:" + str(res_3['lscore_info']['level']) + "\n积分:" + str(
            res_3['cscore_info']['vip_score_total']) + "\nV力值:" + str(res_3['lscore_info']['score'])
    except:
        try:
            res_3 = json.loads(response_3.text)
            log = log + "\n腾讯视频领获取积分异常,返回内容:\n" + str(res_3)
            print(res_3)
        except:
            log = log + "\n腾讯视频获取积分异常,无法返回内容"
    url_3 = 'https://vip.video.qq.com/rpc/trpc.query_vipinfo.vipinfo.QueryVipInfo/GetVipUserInfoH5'
    headers_3 = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2104K10AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.7.85.27058',
        'Content-Type': 'text/plain;charset=UTF-8',
        'cookie': cookie
    }
    data = '{"geticon":1,"viptype":"svip|nfl","platform":8}'
    response_3 = requests.post(url_3, data=data, headers=headers_3)
    try:
        res_3 = json.loads(response_3.text)
        log = log + "\n到期时间:" + str(
            res_3['endTime'])
        if res_3['endmsg'] != '':
            log = log + '\nendmsg:' + res_3['endmsg']
        print(log)
    except:
        try:
            res_3 = json.loads(response_3.text)
            log = log + "\n腾讯视频领获取积分异常,返回内容:\n" + str(res_3)
            print(res_3)
        except:
            log = log + "\n腾讯视频获取积分异常,无法返回内容"
    # 签到
    url_1 = 'https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/CheckIn?rpc_data=%7B%7D'
    headers_1 = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2104K10AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.7.85.27058',
        'Content-Type': 'application/json',
        'referer': 'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
        'cookie': cookie
        }
    response_1 = requests.get(url_1, headers=headers_1)
    try:
        res_1 = json.loads(response_1.text)
        log = log + "\n签到获得v力值:" + str(res_1['check_in_score'])
        print(res_1)
    except:
        try:
            res_1 = json.loads(response_1.text)
            log = log + "\n腾讯视频签到异常，返回内容：\n" + str(res_1)
            print(res_1)
        except:
            log = log + "\n腾讯视频签到异常，无法返回内容"
    # 观看
    url_2 = 'https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/ProvideAward?rpc_data=%7B%22task_id%22:1%7D'
    headers_2 = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2104K10AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.7.85.27058',
        'Content-Type': 'application/json',
        'referer': 'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
        'cookie': cookie
        }
    response_2 = requests.get(url_2, headers=headers_2)
    try:
        res_2 = json.loads(response_2.text)
        log = log + "\n观看获得v力值:" + str(res_2['provide_value'])
        print(res_2)
    except:
        try:
            res_2 = json.loads(response_2.text)
            log = log + "\n腾讯视频领取观看v力值异常,返回内容:\n" + str(res_2)
            print(res_2)
        except:
            log = log + "\n腾讯视频领取观看v力值异常,无法返回内容"
 
    #任务状态
    url = 'https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/ReadTaskList?rpc_data=%7B%22business_id%22:%221%22,%22platform%22:3%7D'
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2104K10AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.7.85.27058',
               'Content-Type': 'application/json',
               'referer': 'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
               'cookie': cookie}
    response = requests.get(url, headers=headers)
    res = json.loads(response.text)

    try:
        lis=res["task_list"]
        log = log + '\n-------v力值任务状态--------'
        for i in lis:
            if i["task_button_desc"]=='已完成':
                log=log+'\n'+i["task_maintitle"]+'\n状态:'+i["task_subtitle"]
    except:
        log = log + "获取状态异常，可能是cookie失效"
        print(res)

    # PushPlus 推送
    push_count = 0
    if push == '1':
        if push_count == 0:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            headers = {'Content-Type': 'application/json'}
            payload = {'token': pp_token, 'title': pp_topic + ' ' + now, 'content': log.strip()}
            r = requests.post('https://www.pushplus.plus/send', data=json.dumps(payload), headers=headers)
            push_count += 1
            if r.status_code == 200:
                print(r.text)
            else:
                print('Push Plus 推送失败')
                print(r.text)
        else:
            print('今天已经发送过消息，不再推送')
    else:
        print('不推送')

 # 推送到企业微信
    print(push_a(log))

def push_a(content):
    if wechat_push == '0':
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
