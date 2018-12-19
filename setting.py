# -*- coding: utf-8 -*- 

##########################################################
#              Rutap Bot 2019 Setting Module             #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
#             GNU General Public License v3.0            #
##########################################################

"""
    [여는 말]
    저희 팀의 소스를 사용 해 주셔서 감사합니다!
    저희 소스의 라이선스는 GNU General Public License v3.0 로써, 사용시 꼭 레포지토리 링크를 기재해야 합니다.
    저희 봇 소스를 이용하여 봇을 돌리실 경우, "HwaHyang - Official#4037"로 연락주시면 감사하겠습니다!
    언제든지 문의사항이 있으시면 https://invite.gg/rutapbot 으로 부탁드립니다!

    [접두사(self.prefix) 권장사항]
    01. 접두사는 '한글자'로 해주세요. (루탑봇의 접두사에 맞게 설정을 하였기에, 두글자 이상으로 하시면 main.py 전체를 수정하셔야 합니다.)
    02. `는 되도록이면 접두사에 넣지 말아주세요. (도움말하고 충돌날 수 있습니다.)

    [봇 관리자 설정(self.owner_id) 유의사항]
    01. 봇 관리자는 한명만 설정 할 수 있습니다. 만약 봇 관리자가 여러명일 경우에는 대표 한명의 ID만 넣어주세요.

    [온라인 알림 채널 설정(self.online_notice_channel) 안내]
    01. 봇이 온라인임을 15분마다 전송할 채널 ID를 넣어주세요.

    [저작권 고지(self.copy) 안내]
    01. 도움말 같은 모든 명령어 하단에 들어가는 \"© 2018 Team. 화공\"을 의미합니다.

    [참고하세요]
    01. 모든 구문 파일에서 "외부 소스 사용함" 이라는 주석이 달려져 있는 구문은 다른 소스의 구문이 일부 포함된 구문입니다. 해당 구문은 저희 라이선스와 별개로 적용이 되오니, 반드시 원 레포지토리를 찾아가서 라이선스를 확인하시기 바랍니다. (모든 구문 출처는 정보에 명시되어 있습니다.)
"""

import datetime

class Settings:
    def __init__(self):
        self.token = "Your_Token"
        self.prefix = ","
        self.owner_id = "Your_ID"
        self.log_file = "msg_log.rtl"
        self.actvity_log_file = "actvity_log.rtl"
        self.online_notice_channel = "Your_Channel"
        self.version = "2019 BETA"
        self.copy = "© 2018-%s Team. 화공" % datetime.datetime.now().year
