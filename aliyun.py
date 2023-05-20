#!/usr/bin/python3
# -- coding: utf-8 --
# @Time : 2023/4/8 10:23
# -------------------------------
# cron "30 5 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('阿里云盘签到');

import json
import requests
import os
from datetime import datetime

# 定义多组账号信息并存储到列表中
accounts = [
    {'name': '账号1', 'refresh_token': '6cb2e4c101f944b59558f07dfc595954'},
    {'name': '账号2', 'refresh_token': '6cb2e4c101f944b59558f07dfc595954'}
]

pp_push = 1  # 是否 Push Plus 推送，1为是，0为否
pp_token = 'f62e59644fac404cae0fea8df8f96d3d'  # Push Plus 推送的 token
pp_topic = '阿里☁盘签到'  # Push Plus 推送的主题

wechat_push = 1  # 是否企业微信推送，1为是，0为否
wx_corpid = 'ww7606bbf6c1cccea9' # 企业ID
wx_secret = 'CxY9TMEe-zsnUrGYXgS6au_hJpKJtUYd_kNiWBSh-X8' # 应用的凭证密钥
wx_agentid = '1000002' # 应用id

# Push+推送
def Push(contents, account_info):
    if pp_push:
        token = pp_token
        headers = {'Content-Type': 'application/json'}
        contents = f"{account_info}\n{contents}"
        contents = contents.replace("(", "").replace(")", "")
        json = {"token": token, 'title': pp_topic, 'content': contents, "template": "txt"}
        resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
        print('Push+ 推送成功' if resp['code'] == 200 else 'Push+ 推送失败')
    # 企业微信推送
    if wechat_push:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + wx_corpid + '&corpsecret=' + wx_secret
        access_token = requests.get(url)
        access_token = eval(access_token.text)
        access_token = access_token.get("access_token")
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": wx_agentid,
            "text": {
                "content": f'阿里☁盘签到\n{contents}'
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, json=data, headers={'Content-Type': 'application/json'}, timeout=100)
        if resp.json().get('errcode') == 0:
            print('企业微信推送成功')
        else:
            print(f"企业微信推送失败：{resp.json()['errmsg']}")
#签到           
def daily_check(access_token):
    url = 'https://member.aliyundrive.com/v1/activity/sign_in_list'
    headers = {
        'Authorization': access_token
    }
    response = requests.post(url=url, headers=headers, json={}).text
    result = json.loads(response)
    if 'success' in result:
        #print('签到成功')
        for i, j in enumerate(result['result']['signInLogs']):
            if j['status'] == 'miss':
                day_json = result['result']['signInLogs'][i - 1]
                # print(day_json)
                if not day_json['isReward']:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    contents = f'{timestamp}\n🎉签到成功，今日未获得奖励'
                else:
                    contents = '本月累计签到{}天,今日签到获得{}{}'.format(result['result']['signInCount'],
                                                                     day_json['reward']['name'],
                                                                     day_json['reward']['description'])
                print(contents)

                return contents

# 使用 refresh_token 更新 access_token
def update_token(refresh_token):
    url = 'https://auth.aliyundrive.com/v2/account/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url=url, json=data).json()
    access_token = response['access_token']
    #         print('获取的access_token为{}'.format(access_token))
    return access_token

# 主函数
def main():
    for i, account in enumerate(accounts):
        print(f'开始处理第 {i+1} 个账号：{account["name"]}')

        # 更新当前账号的 access_token
        access_token = update_token(account['refresh_token'])

        # 执行签到操作
        content = daily_check(access_token)

        # 推送签到结果，并包含账号信息
        if pp_token != '':
            account_info = f'当前处理:{account["name"]}'
            Push(content, account_info)
if __name__ == '__main__':
    main()
