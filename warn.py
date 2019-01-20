# -*- coding:utf-8 -*- 

##########################################################
#              Rutap Bot 2019 Warn Module                #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
#                   BSD 3-Clause License                 #
##########################################################

import os
from activity_log import log_actvity

def warn_give(message, mention_id):
    if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
        f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'r')
        past_warn = f.read()
        f.close()
        now_warn = int(past_warn) + int(1)
        now_warn = str(now_warn)
        f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'w')
        f.write(now_warn)
        f.close()
        log_actvity("%s has gived %s's warn (now : %s)" % (message.author.id, mention_id, now_warn))
        return now_warn
    else:
        f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'w')
        f.write(str(1))
        f.close()
        log_actvity("%s has gived %s's warn (now : 1)" % (message.author.id, mention_id))
        return "1"

def warn_cancel(message, mention_id):
    if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
        f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'r')
        past_warn = f.read()
        f.close()
        now_warn = int(past_warn) - int(1)
        now_warn = str(now_warn)
        f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'w')
        f.write(now_warn)
        f.close()
        log_actvity("%s has removed %s's warn (now : %s)" % (message.author.id, mention_id, now_warn))
        return now_warn
    else:
        return False

def warn_reset(message, mention_id):
    if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
        os.remove("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id))
        log_actvity("%s has reset %s's warn" % (message.author.id, mention_id))
        return None
    else:
        return False

def warn_check_nomention(message, mention_id):
    if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
        f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'r')
        warn_num = f.read()
        f.close()
        log_actvity("%s has confirmed %s's warning. (warn_num : %s)" % (message.author.id, mention_id, warn_num))
        return warn_num
    else:
        log_actvity("%s has confirmed %s's warning. (warn_num : 0)" % (message.author.id, mention_id))
        return "0"

def warn_check_yesmention(message, mention_id):
    if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
        f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'r')
        warn_num = f.read()
        f.close()
        log_actvity("%s has confirmed his warning. (warn_num : %s)" % (message.author.id, warn_num))
        return warn_num
    else:
        log_actvity("%s has confirmed his warning. (warn_num : 0)" % (message.author.id))
        return "0"