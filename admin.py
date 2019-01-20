# -*- coding:utf-8 -*- 

##########################################################
#              Rutap Bot 2019 Admin Module               #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
#                   BSD 3-Clause License                 #
##########################################################

import os, re
from activity_log import log_actvity

def change_presence(message):
    playing = message.content[17:]
    if playing == "":
        return None
    else:
        log_actvity("Change rpc to %s (Request by. %s)." % (playing, message.author.id))
        f = open("rpc.rts", 'w')
        f.write(playing)
        f.close()
        return playing

def user_ban(message):
    q = re.findall(r'\d+', message.content[16:])
    q = q[0]
    q = str(q)
    if q == message.author.id:
        return False
    else:
        open("%s_Banned.rts" % (q), 'w').close()
        log_actvity("I'll Ban %s. (Request by. %s)." % (q, message.author.id))
        return q

def user_unban(message):
    q = re.findall(r'\d+', message.content[16:])
    q = q[0]
    q = str(q)
    if os.path.isfile("%s_Banned.rts" % (q)):
        os.remove("%s_Banned.rts" % (q), 'w')
        log_actvity("I'll UnBan %s. (Request by. %s)." % (q, message.author.id))
        return q
    else:
        return False

def notice_set(message):
    f = open("notice_memo.rts", 'w')
    f.write(message.content)
    f.close()
    log_actvity("I set Notice memo. (Content : %s)." % (message.content))
    return True