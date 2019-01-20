# -*- coding:utf-8 -*- 

##########################################################
#              Rutap Bot 2019 Warn Module                #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
#                   BSD 3-Clause License                 #
##########################################################

import requests, setting
from activity_log import log_actvity

Setting = setting.Settings()

def upload(file_name):
    url = Setting.hangul_clock_upload + "upload.php"
    files = {'myfile': open(file_name, 'rb')}
    r = requests.post(url, files=files)
    log_actvity("I completed Uploading Clock (Link : %sclocks/%s | Logs : %s)" % (Setting.hangul_clock_upload, file_name, r.text))
    return r.text