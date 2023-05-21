import requests
import time

# 在下面添加token
accounts = [
    {'refresh_token': '6cb2e4c101f944b59558f07dfc595954', 'nickname': '账号1'},
    {'refresh_token': '6cb2e4c101f944b59558f07dfc595954', 'nickname': '账号2'}
]

#企业微信
wechat_push = 0 # 是否启用企业微信应用推送功能，1表示启用；0表示禁用
wx_corpid = 'ww7606bbf6c1cccea9' # 企业ID
wx_secret = 'CxY9TMEe-zsnUrGYXgS6au_hJpKJtUYd_kNiWBSh-X8' # 应用的凭证密钥
wx_agentid = '1000002' # 应用id

#push+
pushplus_push = 1 # 是否启用Push+推送，1表示启用；0表示禁用
pushplus_token = 'f62e59644fac404cae0fea8df8f96d3d' # Push+ 的推送 token


class AliyunSignIn(object):
    def __init__(self, refresh_token, nickname):
        self.refresh_token = refresh_token
        self.nickname = nickname

    def get_access_token(self):
        url = 'https://auth.aliyundrive.com/v2/account/token'
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        data = {
            "grant_type": "refresh_token",
            "app_id": "pJZInNHN2dZWk8qg",
            "refresh_token": self.refresh_token
        }
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            self.access_token = f'Bearer {res.json()["access_token"]}'
            self.nick_name = res.json()['nick_name']
            return True
        return False

    def sign_in(self):
        print(f'开始获取账号【{self.nickname}】的access_token')
        if_ = self.get_access_token()
        print(f'正在运行【{self.nickname}】的access_token获取完成{self.nick_name}\n开始签到')
        if not if_:
            print(f'正在运行【{self.nickname}】的获取access_token失败')
        url = 'https://member.aliyundrive.com/v1/activity/sign_in_list'
        headers = {
            "Content-Type": "application/json",
            'Authorization': self.access_token,
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'
        }
        data = {}
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200 and res.json()['success']:
            res_json = res.json()
            notice = ''
            prefix = ''
            for l in res_json['result']['signInLogs']:
                if l['status'] != 'miss':
                    prefix = f'第{l["day"]}天'
                    reward_desc = l['reward']['description'] if l['reward'] else ''
                    notice = l['notice'] + ' ' + reward_desc if l['notice'] else reward_desc
            timestamp = int(time.time())
            timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            notifyStr = f'🎉{prefix}签到成功'
            notifyStr += f' \n{timestamp_str}'

            if notice:
                notifyStr = f'{notifyStr},获得【{notice}】'
            print(f'正在运行【{self.nickname}】的{notifyStr}')

            # push+推送功能
            if pushplus_push:
                pushplus_url = "http://www.pushplus.plus/send"
                pushplus_data = {
                    "token": pushplus_token,
                    "title": "阿里☁盘签到",
                    "content": f'正在运行：{self.nickname}\n{notifyStr}'
                }
                pushplus_resp = requests.post(pushplus_url, json=pushplus_data)
                if pushplus_resp.json().get("code") == 200:
                    print('push+推送成功')
                else:
                    print(f"Push+ 推送失败：{pushplus_resp.json()['msg']}")
            # 企业微信推送功能
            if wechat_push:
                url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + wx_corpid + '&corpsecret=' + wx_secret
                access_token = requests.get(url)
                access_token = eval(access_token.text)
                access_token = access_token.get("access_token")
                url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
                data ={
                        "touser": "@all",
                        "msgtype": "text",
                        "agentid": wx_agentid,
                        "text": {
                            "content": f'阿里☁盘签到\n正在运行：{self.nickname}\n{notifyStr}'
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
            # 打印签到结果
            return True
if __name__ == '__main__':
    for account in accounts:
        ali = AliyunSignIn(account['refresh_token'], account['nickname'])
        ali.sign_in()
