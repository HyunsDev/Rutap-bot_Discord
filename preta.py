# -*- coding: utf-8 -*- 

##########################################################################
#                     Rutap Bot 2019 Timeform Module                     #
# 모든 저작권은 Preta 「 プレタ 」#1614가 소유합니다. 모든 권리를 보유합니다. #
##########################################################################

import time

def timeform(dt1):
    msgtime = str(dt1)
    mili = str(msgtime)[-6:]
    msgtime = str(msgtime)[:-7]
    msgtime = time.strptime(msgtime,'%Y-%m-%d %H:%M:%S')
    msgtime = time.mktime(msgtime)
    msgtime = float(str(msgtime)[:-1] + mili)
    return msgtime