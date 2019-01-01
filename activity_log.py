# -*- coding: utf-8 -*- 

###################################################################
#              Rutap Bot 2019 Actvity Logging Module              #
#     모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다.      #
#                  GNU General Public License v3.0                #
###################################################################

import os, datetime, setting

Setting = setting.Settings()
now = datetime.datetime.now()

def log_actvity(log_text):
    if os.path.isfile("log/%s" % (Setting.actvity_log_file)):
        f = open("log/%s" % (Setting.actvity_log_file), 'r')
        old_log_info = f.read()
        f.close()
        log_info = old_log_info + "\n%s / %s / %s | %s : %s | %s" % (now.year, now.month, now.day, now.hour, now.second, log_text)
        f = open("log/%s" % (Setting.actvity_log_file), 'w')
        f.write(log_info)
        f.close()
    else:
        log_info = "%s / %s / %s | %s : %s | %s" % (now.year, now.month, now.day, now.hour, now.second, log_text)
        f = open("log/%s" % (Setting.actvity_log_file), 'w')
        f.write(log_info)
        f.close()
        print("%s 파일을 발견하지 못하여 해당 파일을 생성하였습니다.\n\n==============\n" % ("log/%s" % (Setting.actvity_log_file)))

def log_start_actvity():
    if os.path.isfile("log/%s" % (Setting.actvity_log_file)):
        f = open("log/%s" % (Setting.actvity_log_file), 'r')
        old_log_info = f.read()
        f.close()
        log_info = old_log_info + "\n\n%s / %s / %s | %s : %s | Logging Started.\n" % (now.year, now.month, now.day, now.hour, now.second)
        f = open("log/%s" % (Setting.actvity_log_file), 'w')
        f.write(log_info)
        f.close()
    else:
        log_info = "%s / %s / %s | %s : %s | Logging Started.\n" % (now.year, now.month, now.day, now.hour, now.second)
        f = open("log/%s" % (Setting.actvity_log_file), 'w')
        f.write(log_info)
        f.close()
        print("%s 파일을 발견하지 못하여 해당 파일을 생성하였습니다.\n\n==============\n" % ("log/%s" % (Setting.actvity_log_file)))