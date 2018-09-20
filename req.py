# !/usr/bin/python3
# coding=utf-8

import hashlib
import json
import requests
import time
import datetime
from log import *


class HttpServer:

    host = "http://hao123.com"

    def get(self):
        req = requests.get(self.host)
        logger.info(req.status_code)
        return req.text

    def post(self, data):
        req = requests.post(self.host, data)


if __name__ == '__main__':
    initLog()
    h = HttpServer()
    print(h.get())
