# -*- coding:utf-8 -*- 

##########################################################
#             Rutap Bot 2019 Normal Module               #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
#                   BSD 3-Clause License                 #
##########################################################

import os, time
from preta import timeform
from activity_log import log_actvity

def ping(message):
    if os.path.isfile('no_ping.txt'):
        return False
    else:
        open("no_ping.txt", 'w').close()

        msgarrived = float(str(time.time())[:-3])
        msgtime = timeform(message.timestamp)
        msgdelay = msgarrived - msgtime - 32400
        ping = int(msgdelay * 1000)

        return ping