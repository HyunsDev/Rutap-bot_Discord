# -*- coding: utf-8 -*- 

###################################################################
#              Rutap Bot 2019 Actvity Logging Module              #
#     모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다.      #
#                  GNU General Public License v3.0                #
###################################################################

import os, datetime, setting

Setting = setting.Settings()
now = datetime.datetime.now()

def log_msg(server, server_id, channel, channel_id, usr, usr_tag, usr_id, msg):
    if os.path.isfile("log/%s" % (Setting.log_file)):
        if os.path.isfile("Server_%s/%s_Server_prefix.rts" % (server_id, server_id)):
            f = open("log/%s" % (Setting.log_file), 'r')
            old_log_info = f.read()
            f.close()
            log_info = old_log_info + "\n%s / %s / %s | %s : %s | Server : %s(%s) | Channel : %s(%s) | Author : %s%s(%s) | Message : %s" % (now.year, now.month, now.day, now.hour, now.second, server, server_id, channel, channel_id, usr, usr_tag, usr_id, msg)
            f = open("log/%s" % (Setting.log_file), 'w')
            f.write(log_info)
            f.close()
        else:
            print("메시지 로깅 모듈(msg_log.py)로부터 메시지 로깅을 거부당했습니다.\n사유 : 해당 서버(%s(%s))에 루탑봇이 활성화 되지 않았습니다!\n\n==============\n" % (server, server_id))
    else:
        if os.path.isfile("Server_%s/%s_Server_prefix.rts" % (server_id, server_id)):
            log_info = "%s / %s / %s | %s : %s | Server : %s(%s) | Channel : %s(%s) | Author : %s%s(%s) | Message : %s" % (now.year, now.month, now.day, now.hour, now.second, server, server_id, channel, channel_id, usr, usr_tag, usr_id, msg)
            f = open("log/%s" % (Setting.log_file), 'w')
            f.write(log_info)
            f.close()
            print("%s 파일을 발견하지 못하여 해당 파일을 생성하였습니다.\n\n==============\n" % ("log/%s" % (Setting.log_file)))
        else:
            print("메시지 로깅 모듈(msg_log.py)로부터 메시지 로깅을 거부당했습니다.\n사유 : 해당 서버(%s(%s))에 루탑봇이 활성화 되지 않았습니다!\n\n==============\n" % (server, server_id))

def log_start_msg():
    if os.path.isfile("log/%s" % (Setting.log_file)):
        f = open("log/%s" % (Setting.log_file), 'r')
        old_log_info = f.read()
        f.close()
        log_info = old_log_info + "\n\n%s / %s / %s | %s : %s | Logging Started.\n" % (now.year, now.month, now.day, now.hour, now.second)
        f = open("log/%s" % (Setting.log_file), 'w')
        f.write(log_info)
        f.close()
    else:
        log_info = "%s / %s / %s | %s : %s | Logging Started.\n" % (now.year, now.month, now.day, now.hour, now.second)
        f = open("log/%s" % (Setting.log_file), 'w')
        f.write(log_info)
        f.close()
        print("%s 파일을 발견하지 못하여 해당 파일을 생성하였습니다.\n\n==============\n" % ("log/%s" % (Setting.log_file)))