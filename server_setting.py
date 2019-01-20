# -*- coding:utf-8 -*- 

##########################################################
#         Rutap Bot 2019 Server Setting Module           #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
#                   BSD 3-Clause License                 #
##########################################################

import os
from activity_log import log_actvity

def prefix_change(message, prefix):
    prefix_change = message.content[5:6]
    if prefix_change == "`":
        return False
    else:
        open("Server_%s/%s_Server_prefix.rts" % (message.server.id, message.server.id), 'w').write(prefix_change)
        log_actvity("%s has changed prefix to %s in %s (was : %s)" % (message.author.id, prefix_change, message.server.id, prefix))
        return prefix_change

def cc_delete(message):
    if os.path.isfile("Server_%s/%s_Server_%s_Query.rtl" % (message.server.id, message.server.id, message.author.id)):
        return False
    else:
        if message.content[7:] == "":
            return "Invaild"
        else:
            if os.path.isfile("Server_%s/%s_Server_CC_%s.rts" % (message.server.id, message.server.id, message.content[7:])):
                limit = float(open("Server_%s/%s_Server_CC_Limit.rtl" % (message.server.id, message.server.id), 'r').read())
                open("Server_%s/%s_Server_CC_Limit.rtl" % (message.server.id, message.server.id), 'w').write(str(limit + 1.0))
                os.remove("Server_%s/%s_Server_CC_%s.rts" % (message.server.id, message.server.id, message.content[7:]))
                return message.content[7:]

def welcome_message(message):
    if message.content[5:].startswith('끄기'):
        if os.path.isfile("Server_%s/%sServer_welcome_say_channel.rts" % (message.server.id, message.server.id)):
            os.remove("Server_%s/%sServer_welcome_say_channel.rts" % (message.server.id, message.server.id))
            os.remove("Server_%s/%sServer_welcome_msg.rts" % (message.server.id, message.server.id))
            log_actvity("%s has off the welcome message." % (message.author.id))
            return "Delete"
        else:
            return False
    else: 
        welcome_msg = message.content[5:]
        open("Server_%s/%sServer_welcome_say_channel.rts" % (message.server.id, message.server.id), 'w').write(message.channel.id)
        open("Server_%s/%sServer_welcome_msg.rts" % (message.server.id, message.server.id), 'w').write(welcome_msg)
        log_actvity("%s has set the welcome message. (msg : (Mention), %s)" % (message.author.id, welcome_msg))
        return welcome_msg

def bye_message(message):
    if message.content[6:].startswith('끄기'):
        if os.path.isfile("Server_%s/%sServer_bye_say_channel.rts" % (message.server.id, message.server.id)):
            os.remove("Server_%s/%sServer_bye_say_channel.rts" % (message.server.id, message.server.id))
            os.remove("Server_%s/%sServer_bye_msg.rts" % (message.server.id, message.server.id))
            log_actvity("%s has off the bye message." % (message.author.id))
            return "Delete"
        else:
            return False
    else: 
        bye_msg = message.content[6:]
        open("Server_%s/%sServer_bye_say_channel.rts" % (message.server.id, message.server.id), 'w').write(message.channel.id)
        open("Server_%s/%sServer_bye_msg.rts" % (message.server.id, message.server.id), 'w').write(bye_msg)
        log_actvity("%s has set the bye message. (msg : (Mention), %s)" % (message.author.id, bye_msg))
        return bye_msg