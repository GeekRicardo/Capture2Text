# -*- coding: utf-8 -*-
# @Author: GeekRicardo
# @Date:   2019-10-25 16:49:01
# @Last Modified by:   GeekRicardo
# @Last Modified time: 2019-10-27 19:41:50

from bs4 import BeautifulSoup as bs
import requests
import pdb
import time
import random
import hashlib
import json
import urllib


class translate():

    def __init__(self):
        pass

    def Tranlate_word(self, word):
        """翻译一个单词

        Arguments:
                word {str} -- 单词
        """
        r = {}
        r['error'] = ''

        url = "http://dict.youdao.com/w/" + word.rstrip()
        res = requests.get(url)
        if(res == None):
            return None
        html = res.text
        soup = bs(html, "html.parser")
        resultHtml = bs(str(soup.find('div', id='phrsListTab')), "html.parser")
        try:
            r['keyword'] = resultHtml.find("span", class_="keyword").string
        except Exception:
            print('未知错误，查询"keyword"失败！')
            return None
        # 获取发音
        phonetic = []
        try:
            taglist = resultHtml.find_all("span", class_="phonetic")
        except:
            print('未知错误，查询发音失败！')
            return None
        for tag in taglist:
            phonetic.append(tag.string)
        r['phonetic'] = phonetic
        # 获取详细释义
        try:
            shiyiHtml = bs(
                str(resultHtml.find('div', class_='trans-container')), "html.parser")
        except Exception:
            print('未知错误，获取详细释义失败！')
            return None
        try:
            shiyi = shiyiHtml.find('ul').get_text()
        except:
            print('未知错误，获取详细释义失败！')
            return None
        wordclass = ['n.', 'vt.', 'vi.', 'adj.', 'adv.', 'prep.', 'conj.',
                     'det.', 'int.', 'pron.', 'pl.', 'inter.', 'num.', 'misc.']
    # pdb.set_trace()
        shiyi = shiyi.replace('\n', ' ')
        for item in wordclass:
            shiyi = shiyi.replace(item, ' (' + item + ')')
        r['paraphrase'] = shiyi
        return r

    def Translation_Sentence(self, phrase):
        '''翻译一个句子

        Arguments:
                phrase {str} -- 句子

    Returns:
                str -- result
        '''
        url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

        data = {
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'version': 2.1,
            'bv': 'e218a051a7336600dfed880d272c7d6f',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
            'doctype': 'json'
        }

        u = 'fanyideskweb'
        d = phrase
        timestamp = str(int(time.time() * 1000))
        f = timestamp + str(random.randint(1, 10))
        c = "n%A-rKaT5fb[Gy?;N5@Tj"

        sign = hashlib.md5((u + d + f + c).encode('utf-8')).hexdigest()

        data['i'] = phrase
        data['client'] = 'fanyideskweb'
        data['salt'] = f
        data['sign'] = sign
        data['ts'] = timestamp
        # data = urllib.parse.urlencode(data).encode('utf-8')

        print(data)

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        headers = {"User-Agent": user_agent,
                   'Referer': 'http://fanyi.youdao.com/?keyfrom=dict2.index',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Origin': 'http://fanyi.youdao.com'}
        r = requests.get(
            'http://fanyi.youdao.com/?keyfrom=dict2.index', headers=headers)
        # requests.get('http://rlogs.youdao.com/rlog.php?_npid=fanyiweb&_ncat=event&_ncoo=53428611.87561828&_nssn=NULL&_nver=1.2.0&_ntms='+ str(int(time.time() * 1000) +'&_nhrf=newweb_translate_text&keyfrom=dict2.index')
        res = requests.post(url=url, data=data, cookies=r.cookies)
        print(res.text)
        pdb.set_trace()
        dict = eval(res.text)
        print(dict)
        if(dict['errorCode'] != 0):
            print(content, "没有查询到结果，请再试一次！", 0)
            return None
        result = str(dict['translateResult'])[2:-2]
        return result

    def fomatwordresult(self, word):
        s = ''
        if(result['error'] != '' and result['error'] != None):
            return result['error']
        else:
            s += ("**> +" + '\n')
            s += ('**> |\t' + result['keyword'] + ' 查询结果  |' + '\n')
            s += ("**> +" + '\n')
            if result['phonetic'] != '':
                s += ('**> |发音： ')
                for fayin in result['phonetic']:
                    s += (' ' + fayin + ' ')
            s += ("\n**> |" + '\n')
            s += ('**> +' + '\n')
            s += ('**> |' + result['paraphrase'] + '\n')
            s += ("**> |" + '\n')
            s += ("**> +" + '\n')
            s += ("**> |" + '\n')
        return s
