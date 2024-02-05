from urllib import request

import requests
import os
import re
import json
from fake_useragent import UserAgent


class Baidu_Translate:
    def __init__(self):
        self.session = request.Session()
        self.session.headers = {
            'User-Agent': UserAgent().random,
            "Host": "fanyi.baidu.com",
            "X-Requested-With": "XMLHttpRequest",
            # "sec-ch-ua": '"Not?A_Brand";="8","Chromium";v="108","Microsoft Edge";V="108",
            #              "sec-ch-ua-mobile":"?0",
            #                                 "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Connection": "keep-alive",
        }

        self.session.get("https://fanyi.baidu.com")
        res = self.session.get("https://fanyi.baidu.com").content.decode()
        self.token = re.findall(r"token: '(.*)',", res, re.M)[0]

    def generate_sign(self, query):
        try:
            if os.path.isfile("./baidu.js"):
                with open("./baidu.js", 'r', encoding="utf-8") as f:
                    baidu_js = f.read()
            ctx = execjs.compile(baidu_js)
            return ctx.call('b', query)
        except Exception as e:
            print(e)


    def lang_detect(self, src: str) -> str:
        url = "https://fanyi.baidu.com/langdetect"
        fromLan = self.session.post(url, data={"query": src}).json()["lan"]
        return fromLan


    def translate(self, query: str, toLan: str = "", fromLan: str = "") -> str:
        if fromLan == "":
            fromLan = self.lang_detect(query)

        if toLan == "":
            toLan = "zh" if fromLan != "zh" else "en"

        url = 'https://fanyi.baidu.com/v2transapi'
        sign = self.generate_sign(query)
        data = {
            "from": fromLan,
            "to": toLan,
            "query": query,
            "transtype": "translang",
            "simple_means_flag": "3",
            "sign": sign,
            "token": self.token,
            "domain": "common"
        }
        tryTimes = 0
        try:
            while tryTimes < 100:
                res = self.session.post(
                    url=url,
                    params={"from": fromLan, "to": toLan},
                    data=data,
                )
                if "trans_result" in res.text:
                    break
                tryTimes += 1
            return res.json().get("trans_result").get("data")[0].get("dst")
        except Exception as e:
            print(e)

    def test(self):
        url = 'https://fanyi.baidu.com/v2transapi'
        sign = self.generate_sign("你好")
        data = {
            "from": "zh",
            "to": ' en',
            "query": "你好",
            "transtype": "translang",
            "simple_means_flag": "3",
            "sign": sign,
            "token": self.token,
            "domain": "common"
        }
        res = requests.post(
            url=url,
            params={"from": "zh", "to": 'en'},
            data=data,
            headers={
                'User-Agent': UserAgent().random,
            }
        )
        res.json()


if __name__ == "__main__":
    baidu_tran = Baidu_Translate()
    sign = baidu_tran.generate_sign("你好")
