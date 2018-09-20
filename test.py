# !/usr/bin/python3
# coding=utf-8

import hashlib
import json
import requests
import time
import datetime


class PostServices:
    """一个简单的类实例"""
    host = "http://192.168.143.251:81"
    appkey = "cf85e34a"
    secret = "d0927c5416a94c189cd34933be94c256"

    def __init__(self):
        pass

    def Get(self, url):
        """
        self.Get(url,data）
        :param url:
        :param data:
        :return:
        """
        req = requests.get(url)  # GET方法
        return req.text

    def Post(self, url, data):
        """
        self.Post(url,data）
        :param url:
        :param data:
        :return:
        """
        headers = {
            'X-AjaxPro-Method': 'ShowList',
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': str(len(data))
        }

        # data = parse.urlencode(data).encode('utf-8')
        # data1 = json.loads(data)
        # data = urllib.parse.urlencode(data1).encode(encoding='UTF8')
        req = requests.post(url=url, data=data, headers=headers, timeout=20)
        # page = request.urlopen(req).read()
        # page = page.decode('utf-8')
        return req.text

    def getHikToken(self, url_param, str, secret):
        m = hashlib.md5()
        strs = url_param + str + secret
        m.update(strs.encode("utf8"))
        s = m.hexdigest()
        return s.upper()

    def getMillisecond(self):
        t = time.time()
        v = (int(round(t * 1000)))
        return v

    def getFloorNullNum(self):
        host = self.host
        url_param = "/openapi/service/pms/status/getLeftParkingPlots"
        api = host + url_param
        appkey = self.appkey
        secret = self.secret
        uuid = self.getUid(host, appkey, secret)
        pageNo = 1;
        pageSize = 100;
        time = self.getMillisecond()
        data_token = {
            "appkey": appkey,
            "time": time,
            "pageNo": pageNo,
            "pageSize": pageSize,
            "opUserUuid": uuid
        }
        data_token = str(json.dumps(data_token))
        token = self.getHikToken(url_param, data_token, secret)
        api = api + "?token=" + token
        res = self.Post(api, data_token)
        return self.reData(res)

    def getUid(self, host, appkey, secret):
        url_param = "/openapi/service/base/user/getDefaultUserUuid"
        api = host + url_param
        time = self.getMillisecond()
        time = str(time)
        data_token = {
            "appkey": appkey,
            "time": time
        }
        data_token = str(json.dumps(data_token))

        token = self.getHikToken(url_param, data_token, secret)

        api = api + "?token=" + token
        res = self.reData(self.Post(api, data_token))

        return res['data'];

    def getParkNum(self):
        url = "http://120.26.39.165:28006/api/v1/park-num"
        cont = self.Get(url)
        park_arr = self.reData(cont)
        under_car = park_arr['data'];

        inner_num = self.getFloorNullNum()
        floor_car = inner_num['data']['list']

        all_floor_leftnum = 0

        for v in floor_car:
            all_floor_leftnum += int(v['leftNum'])

        data = {
            "all": under_car['space_total'],
            "overground_cars": {
                "parkName": "苏州奥体中心",
                "floorName": "地上",
                "leftNum": under_car['space_empty'] - all_floor_leftnum
            },
            "floor_car": floor_car
        }
        return str(json.dumps(data))

    def reData(self, data):
        return json.loads(data)


# 实例化类
h = PostServices()
res = h.getParkNum();
data = {
    "cont": res
}
api = "http://120.26.39.165:28006/api/v1/insert_num";

r = h.Post(api, json.dumps(data));
print(res)
