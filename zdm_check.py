# -*- coding: utf8 -*-
import json
	
import time


"""
Serverless值得买自动签到脚本
@author : OKC
"""
import requests
from sys import argv

import config
import logging
from PushMessage import PushMessage

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies    

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content


def main(*args):
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["ZDM_COOKIES"]
    #with open('data.json','r',encoding='utf-8') as fp:
        #configData = json.load(fp)
    #cookies = configData["cookie"]

    pm = PushMessage(title="ZDM签到", token=os.environ["PUSH_PLUS_TOKEN"])
    
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    print(res)
    
    pm.addMsg(f'errcode:{res["error_code"]}')
    data = res["data"]
    pm.addMsg(f'连续签到：{data["checkin_num"]}天')
    pm.addMsg(f'补签卡：{data["cards"]}张')
    #pm.addMsg(f'日志：{res}')
    print(pm.getMsg())
    try:
        pm.pushMessage()
    except Exception as e: 
        logging.warning(f'消息推送异常，原因为{str(e)}')
    
