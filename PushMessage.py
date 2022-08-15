class PushMessage(object):
    "消息推送"
    def __init__(self, title, SCKEY=None, email=None, token=None):
        "初始化"
        self.__title = title
        self.__message = ""
        self.__send_serverchan = f'https://sc.ftqq.com/{SCKEY}.send' if SCKEY else None
        self.__send_email = f'http://liuxingw.com/api/mail/api.php?address={email}' if email else None
        self.__send_pushplus=f'http://www.pushplus.plus/send?token={token}' if token else None
        self.__title = title
        self.__message = ""

    def sendText(self, text, desp):
        "发送消息"
        import requests
        if self.__send_email:
            res = requests.get(self.__send_email, params={"name": text,"certno": desp.replace("\n","<br>")})
            print(res)

        if self.__send_serverchan:
            requests.post(self.__send_serverchan, data={"text": text,"desp": desp})
        
        if self.__send_pushplus:
            requests.get(self.__send_pushplus, params={"title": text,"content": desp.replace("\n","<br>")})


    def addMsg(self, msg, newLine=True):
        "添加要推送的消息"
        self.__message = f"{self.__message}{msg}\n" if newLine else f"{self.__message}{msg}"

    def pushMessage(self):
        "推送已经添加消息"
        self.sendText(self.__title, self.__message)
    
    def setMsg(self, msg):
        "设置要推送的消息"
        self.__message = msg

    def getMsg(self):
        "获取要推送的消息"
        return self.__message

    def setTitle(self, title):
        "设置消息标题"
        self.__title = title

    def getTitle(self):
        "获取当前消息标题"
        return self.__title
