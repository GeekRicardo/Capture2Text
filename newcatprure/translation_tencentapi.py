# -*- coding: utf-8 -*-
# @Author: GeekRicardo
# @Date:   2019-10-25 19:36:22
# @Last Modified by:   GeekRicardo
# @Last Modified time: 2019-10-25 21:00:09


import requests
import json
from PIL import Image
import io
import base64
import time
import uuid
import random
import hashlib


class translation():

    def __init__(self):
        self.url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_imagetranslate'
        self.appkey = '50g2a4BLTvQJKTBb'
        self.data = {
            'app_id': '2123255879',
            'scene': 'doc'
        }

    def en_2_zh(self, img):
        self.data['source'] = 'en'
        self.data['target'] = 'zh'
        # output_buffer = io.BytesIO()
        # img.save(output_buffer, format='JPEG')
        # byte_data = output_buffer.getvalue()
        self.data['image'] = base64.b64encode(img).decode('ascii')
        self.data['session_id'] = random.choice(range(1000, 10000))
        self.data['time_stamp'] = str(int(time.time()))
        self.data['nonce_str'] = str(uuid.uuid1())[10:-10]
        self.data['sign'] = self.get_sign(self.data)

        res = requests.post(url=self.url, data=self.data)
        print(res.text)
        return res.text

    def get_sign(self, data):
        keys = sorted(data.keys())
        print(data)
        s = ''
        for k in keys:
            if data[k] != '':
                s += (k + '=' + str(data[k]) + '&')
        s += self.appkey
        print(s)
        cs = str(hashlib.md5(s.encode('utf-8')).hexdigest()).upper()
        return cs
