# -*- coding:utf-8 -*-
__author__ = 'lijm'
__date__ = '2017/10/19 上午9:42'

import urllib.request
from urllib.parse import urlparse
import os

global_int = 1

def url_open(url):
    req = urllib.request.Request(url=url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    respones = urllib.request.urlopen(req)
    html = respones.read()
    return html

def parse_html_to_page(html):
    a = html.find('current-comment-page') + 23
    b = html.find(']', a)
    return html[a:b]

def parse_img_url(html):
    img_url = []
    b = 1
    check = True
    while check:
        a = html.find('<img src="', b)
        if a == -1:
            print('-1')
            check = False
        else:
            b = html.find('.jpg', a+10) + 4
            if (b-a) > 255:
                pass
            else:
                img_url.append('https:' + html[a+10:b])

    return img_url


def img_down(img_url, fold):
    global global_int
    for url in img_url:
        # req = urllib.request.Request(url)
        # req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        respones = urllib.request.urlopen(url)
        # img_path = url.split('.')[-1]
        # url_obj = urlparse(img_path)
        img_path = str(global_int) + '.jpg'
        with open(img_path, 'wb') as f:
            f.write(respones.read())
            global_int += 1

def img_downloader(url, fold = 'img_save'):
    os.rmdir(fold)
    os.mkdir(fold)
    os.chdir(fold)

    html = url_open(url).decode('utf-8')
    page = int(parse_html_to_page(html))

    for i in range(20):
        page_now = page - i
        url = 'https://jandan.net/ooxx/page-' + str(page_now) +'#comments'
        html = url_open(url).decode('utf-8')
        img_url = parse_img_url(html)
        img_down(img_url, fold)

if __name__ == '__main__':
    url = 'https://jandan.net/ooxx'
    img_downloader(url=url)