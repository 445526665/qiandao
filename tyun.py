# #!/usr/bin/python3
# # -- coding: utf-8 --
# # @Time : 2023/4/4 9:23
# #作者：https://www.52pojie.cn/thread-1231190-1-1.html
# # -------------------------------
# # cron "30 4 * * *" script-path=xxx.py,tag=匹配cron用
# # const $ = new Env('天翼云盘签到');


import time
import re
import json
import base64
import hashlib
import urllib.parse,hmac
import rsa
import requests
import random
from datetime import datetime

BI_RM = list("0123456789abcdefghijklmnopqrstuvwxyz")
 
B64MAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
 
s = requests.Session()
 

# 在下面添加账号（仅支持手机号）和密码
# 格式为：accounts = ["下面这里账号xxx,下面这里密码xxx,账号1", "xxx,xxx.,账号2", ...]
accounts = [
    "xxx,xxx,账号1",
    "xxx,xxx.,账号2",
]

push = 1  # 是否 Push Plus 推送，1为是，0为否
pp_token = 'xxx'  # Push Plus 推送的 token
pp_topic = '天翼☁签到'  # Push Plus 推送的主题

wechat_push = 0  # 是否企业微信推送，1为是，0为否
corpid = 'xxx' # 企业ID
secret = 'xxx' # 应用的凭证密钥
agentid = 'xxx' # 应用id

def int2char(a):
    return BI_RM[a]
 
def b64tohex(a):
    d = ""
    e = 0
    c = 0
    for i in range(len(a)):
        if list(a)[i] != "=":
            v = B64MAP.index(list(a)[i])
            if 0 == e:
                e = 1
                d += int2char(v >> 2)
                c = 3 & v
            elif 1 == e:
                e = 2
                d += int2char(c << 2 | v >> 4)
                c = 15 & v
            elif 2 == e:
                e = 3
                d += int2char(c)
                d += int2char(v >> 2)
                c = 3 & v
            else:
                e = 0
                d += int2char(c << 2 | v >> 4)
                d += int2char(15 & v)
    if e == 1:
        d += int2char(c << 2)
    return d
  
def rsa_encode(j_rsakey, string):
    rsa_key = f"-----BEGIN PUBLIC KEY-----\n{j_rsakey}\n-----END PUBLIC KEY-----"
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
    result = b64tohex((base64.b64encode(rsa.encrypt(f'{string}'.encode(), pubkey))).decode())
    return result
 
 
def calculate_md5_sign(params):
    return hashlib.md5('&'.join(sorted(params.split('&'))).encode('utf-8')).hexdigest()
 
 
def login(username, password):
    #https://m.cloud.189.cn/login2014.jsp?redirectURL=https://m.cloud.189.cn/zhuanti/2021/shakeLottery/index.html
    url=""
    urlToken="https://m.cloud.189.cn/udb/udb_login.jsp?pageId=1&pageKey=default&clientType=wap&redirectURL=https://m.cloud.189.cn/zhuanti/2021/shakeLottery/index.html"
    s = requests.Session()
    r = s.get(urlToken)
    pattern = r"https?://[^\s'\"]+"  # 匹配以http或https开头的url
    match = re.search(pattern, r.text)  # 在文本中搜索匹配
    if match:  # 如果找到匹配
        url = match.group()  # 获取匹配的字符串
        # print(url)  # 打印url
    else:  # 如果没有找到匹配
        print("没有找到url")
 
    r = s.get(url)
    # print(r.text)
    pattern = r"<a id=\"j-tab-login-link\"[^>]*href=\"([^\"]+)\""  # 匹配id为j-tab-login-link的a标签，并捕获href引号内的内容
    match = re.search(pattern, r.text)  # 在文本中搜索匹配
    if match:  # 如果找到匹配
        href = match.group(1)  # 获取捕获的内容
        # print("href:" + href)  # 打印href链接
    else:  # 如果没有找到匹配
        print("没有找到href链接")
 
    r = s.get(href)
    captchaToken = re.findall(r"captchaToken' value='(.+?)'", r.text)[0]
    lt = re.findall(r'lt = "(.+?)"', r.text)[0]
    returnUrl = re.findall(r"returnUrl= '(.+?)'", r.text)[0]
    paramId = re.findall(r'paramId = "(.+?)"', r.text)[0]
    j_rsakey = re.findall(r'j_rsaKey" value="(\S+)"', r.text, re.M)[0]
    s.headers.update({"lt": lt})
 
    username = rsa_encode(j_rsakey, username)
    password = rsa_encode(j_rsakey, password)
    url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
        'Referer': 'https://open.e.189.cn/',
    }
    data = {
        "appKey": "cloud",
        "accountType": '01',
        "userName": f"{{RSA}}{username}",
        "password": f"{{RSA}}{password}",
        "validateCode": "",
        "captchaToken": captchaToken,
        "returnUrl": returnUrl,
        "mailSuffix": "@189.cn",
        "paramId": paramId
    }
    r = s.post(url, data=data, headers=headers, timeout=5)
    if (r.json()['result'] == 0):
        print(r.json()['msg'])
    else:
        print(r.json()['msg'])
    redirect_url = r.json()['toUrl']
    r = s.get(redirect_url)
    return s
    #Push+
def Push(contents):
    if push:
        token = pp_token
        headers = {'Content-Type': 'application/json'}
        contents = f"{contents} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        contents = contents.replace("(", "").replace(")", "")
        json = {"token": token, 'title': pp_topic, 'content': contents, "template": "txt"}
        resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
        print(resp)
    #企业微信
    if wechat_push:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + secret
        access_token = requests.get(url)
        print(access_token)
        access_token = eval(access_token.text)
        access_token = access_token.get("access_token")
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": agentid,
            "text": {
                "content": '天翼☁签到\n'+contents
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, json=data, headers={'Content-Type': 'application/json'}, timeout=100)
        print(resp.text)

def main():
    for account in accounts:
        account = account.split(",")
        username = account[0]
        password = account[1]
        name = account[2]
        print(f" {name} 签到抽奖结果：")
        s = login(username, password)

        rand = str(round(time.time() * 1000))
        surl = f'https://api.cloud.189.cn/mkt/userSign.action?rand={rand}&clientType=TELEANDROID&version=8.6.3&model=SM-G930K'
        url = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN'
        url2 = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN'
        url3 = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_2022_FLDFS_KJ&activityId=ACT_SIGNIN'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVersion/1.0.6',
            "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
            "Host": "m.cloud.189.cn",
            "Accept-Encoding": "gzip, deflate",
        }
        response = s.get(surl, headers=headers)
        netdiskBonus = response.json()['netdiskBonus']
        if (response.json()['isSign'] == "false"):
            print(f"未签到，签到获得{netdiskBonus}M空间")
        else:
            print(f"已经签到过了，签到获得{netdiskBonus}M空间")

        response = s.get(url, headers=headers)
        if ("errorCode" in response.text):
            res1 = ""
        else:
            description = response.json()['description']
            res1 = f"{name} 抽奖获得{description}"
            print(f"🎉抽奖获得50M空间")

        response = s.get(url2, headers=headers)
        if ("errorCode" in response.text):
            res2 = ""
        else:
            description = response.json()['description']
            res2 = f"{name} 抽奖获得{description}"

        response = s.get(url3, headers=headers)
        if ("errorCode" in response.text):
            res3 = ""
        else:
            description = response.json()['description']
            res3 = f"{name} 链接3抽奖获得{description}"
        message = f"{name} 状态：\n🍩签到获得{netdiskBonus}M空间\n🎉抽奖获得50M空间\n🎉抽奖获得50M空间\n"
        Push(contents=message)

def lambda_handler(event, context):  # aws default
    main()
 
 
def main_handler(event, context):  # tencent default
    main()
 
 
def handler(event, context):  # aliyun default
    main()
 
 
if __name__ == "__main__":
    # time.sleep(random.randint(5, 30))
    main()
