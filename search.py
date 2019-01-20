# -*- coding:utf-8 -*- 

##########################################################
#              Rutap Bot 2019 Search Module              #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
#                   BSD 3-Clause License                 #
##########################################################

import requests, json, random
from activity_log import log_actvity
from bs4 import BeautifulSoup as bs4

def nomal_neko(message):
    #nekos.life API 사용 구문 시점
    r = requests.get("https://nekos.life/api/v2/img/neko")
    r = r.text
    data = json.loads(r)
    file = data["url"]
    #nekos.life API 사용 구문 종점
    log_actvity("I sent %s to %s." % (file, message.author.id))
    return file

def nsfw_neko(message):
    #nekos.life API 사용 구문 시점
    r = requests.get("https://nekos.life/api/v2/img/lewd")
    r = r.text
    data = json.loads(r)
    file = data["url"]
    #nekos.life API 사용 구문 종점
    log_actvity("I sent %s to %s." % (file, message.author.id))
    return file

def img_search(message, q):
    q = q.encode("raw_unicode_escape")
    q = str(q)

    data = requests.get("https://www.google.co.kr/search?q=" + q + "&source=lnms&tbm=isch&sa=X")
    soup = bs4(data.text, "html.parser")
    imgs = soup.find_all("img")

    file = random.choice(imgs[1:])['src']

    log_actvity("I sent %s to %s. (Search query : %s)" % (file, message.author.id, message.content[5:]))
    return file