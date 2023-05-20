import requests
import time

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
            notifyStr = f'🎉{prefix}签到成功'
            timestamp = int(time.time())
            timestamp_str = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(timestamp))
            notifyStr += f' \n{timestamp_str}'
            if notice:
                notifyStr = f'{notifyStr},获得【{notice}】'

            # Add Push+ notification code here
            push_token = 'f62e59644fac404cae0fea8df8f96d3d'
            title = 'AliyunDrive签到'
            content = f'正在运行：{self.nickname}\n{notifyStr}'
            data = {
                'token': push_token,
                'title': title,
                'content': content,
            }
            res = requests.post('http://www.pushplus.plus/send', json=data)
            if res.status_code == 200 and res.json()['code'] == 200:
                print('Push+消息发送成功')
            else:
                print('Push+消息发送失败')

            print(f'正在运行【{self.nickname}】的{notifyStr}')

if __name__ == '__main__':
    accounts = [
        {'refresh_token': '6cb2e4c101f944b59558f07dfc595954', 'nickname': '账号1'},
        {'refresh_token': '6cb2e4c101f944b59558f07dfc595954', 'nickname': '账号2'}
    ] # replace with your list of accounts
    for account in accounts:
        ali = AliyunSignIn(account['refresh_token'], account['nickname'])
        ali.sign_in()
