# -*- coding: utf-8 -*- 

##########################################################
#                  Rutap Bot Main Module                 #
#   Copyright 2018 Team. Hwagong. All Rights Reserved.   #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
##########################################################

import asyncio, discord, random, requests, datetime, os, sys, re
from bs4 import BeautifulSoup as bs
import general_settings

Setting = general_settings.Settings()
app = discord.Client()
bot_deleting = False

# 준비완료
@app.event
async def on_ready():
    #f = open("rpc.txt", 'r', encoding='UTF8')
    f = open("rpc.txt", 'r')
    rpc = f.read()
    f.close()
    print(app.user.name, "(%s)" % app.user.id)
    await app.change_presence(game=discord.Game(name=rpc, type=0))

# 유저입장
@app.event
async def on_member_join(member):
    if os.path.isfile("%sServer_welcome_say_channel" % (
        member.server.id
    )):
        f = open("%sServer_welcome_say_channel" % (
            member.server.id
        ), 'r')
        message_server = f.read()
        f.close()
        f = open("%sServer_welcome_msg" % (
            member.server.id
        ), 'r')
        welcome_msg = f.read()
        f.close()
        await app.send_message(app.get_channel(message_server), "<@" + member.id + ">, %s" % (
            welcome_msg
        ))
    else:
        return None

# 유저퇴장
@app.event
async def on_member_remove(member):
    if os.path.isfile("%sServer_bye_say_channel" % (
        member.server.id
    )):
        f = open("%sServer_bye_say_channel" % (
            member.server.id
        ), 'r')
        message_server = f.read()
        f.close()
        f = open("%sServer_bye_msg" % (
            member.server.id
        ), 'r')
        bye_msg = f.read()
        f.close()
        await app.send_message(app.get_channel(message_server), "<@" + member.id + "> %s" % (
            bye_msg
        ))
    else:
        return None

# 메세지
@app.event
async def on_message(message):

    if os.path.isfile("afk_because" + message.author.id + ".txt"):
        try:
            now = datetime.datetime.now()

            f = open("afk_year" + message.author.id + ".txt", 'r')
            past_year = f.read()
            f.close()

            f = open("afk_month" + message.author.id + ".txt", 'r')
            past_month = f.read()
            f.close()

            f = open("afk_day" + message.author.id + ".txt", 'r')
            past_day = f.read()
            f.close()

            f = open("afk_hour" + message.author.id + ".txt", 'r')
            past_hour = f.read()
            f.close()

            f = open("afk_min" + message.author.id + ".txt", 'r')
            past_min = f.read()
            f.close()

            f = open("afk_because" + message.author.id + ".txt", 'r')
            imafk = f.read()
            f.close()

            os.remove("afk_year" + message.author.id + ".txt")
            os.remove("afk_month" + message.author.id + ".txt")
            os.remove("afk_day" + message.author.id + ".txt")
            os.remove("afk_hour" + message.author.id + ".txt")
            os.remove("afk_min" + message.author.id + ".txt")
            os.remove("afk_because" + message.author.id + ".txt")

            embed = discord.Embed(title="잠수종료!", description="USER : <@" + message.author.id + ">\n\n잠수 시작 시간 : " + str(past_year) + "년 " + str(past_month) + "월 " + str(past_day) + "일 " + str(past_hour) + "시 " + str(past_min) + " 분\n잠수 종료 시간 : " + str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 " + str(now.hour) + "시 " + str(now.minute) + "분\n\n사유 : " + imafk + "", color=0x00ff00)
            await app.send_message(message.channel, embed=embed)  
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)  

    if Setting.prefix + "rutap admin shutdown" == message.content:
        if message.author.id == Setting.owner_id:
            await app.send_message(message.channel, "<@" + message.author.id + ">, Shutdown the Main Module(main.py)!")
            exit()
        else:
            return None

    if Setting.prefix + "rutap admin restart" == message.content:
        if message.author.id == Setting.owner_id:
            await app.send_message(message.channel, "<@" + message.author.id + ">, Restart the Main Module(main.py)!")
            python = sys.executable
            os.execl(python, python, * sys.argv)
        else:
            return None

    if message.content.startswith(Setting.prefix + 'rutap admin game'):
        try:
            if message.author.id == Setting.owner_id:
                playing = message.content[18:]
                if playing == "":
                    embed = discord.Embed(title="Error!", description="game name is null!", color=0xff0000)
                    await app.send_message(message.channel, embed=embed)
                else:
                    embed = discord.Embed(title="", description="Ok. I'll change rpc to : %s" % (
                        playing   
                    ), color=0x00ff00)
                    await app.send_message(message.channel, embed=embed)
                    await app.change_presence(game=discord.Game(name=playing, type=0))
                    f = open("rpc.txt", 'w')
                    f.write(playing)
                    f.close()
            else:
                return None
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    # 가이드
    if Setting.prefix + "도움말" == message.content:
        try:
            embed = discord.Embed(title="명령어!", description="%s정보 - 봇의 정보를 알려줍니다!\n%s핑 - 서버 핑을 출력합니다.\n%s냥이 - 랜덤으로 냥이 짤을 출력합니다!\n%s잠수 [사유] - 잠수 모드로 들어갈 수 있습니다.\n|     단, 채팅을 칠 경우, 잠수가 풀리니 참고하세요.\n%s이미지 [검색어] - 구글에서 아무 이미지나 가져와서 보여줍니다.\n%s익명 [할말] - [할말]에 적은 내용을 봇이 출력합니다!\n~~%s투표 - 투표관련 명령어를 출력합니다.~~ (점검중입니다)\n~~%s경고 - 경고관련 명령어를 출력합니다.~~ (알 수 없는 버그가 발생하여서 작동하지 않습니다)\n%s시간 - 현재 시간을 출력합니다.\n%s서버정보 - 서버의 정보를 불러옵니다.\n%s내정보 - 당신의 정보를 불러옵니다.\n|     아직은 노출할 수 있는 정보가 별로 없지만, 추후 지속적인 업데이트를 통하여 노출되는 정보를 추가할 예정입니다." % (
                Setting.prefix, Setting.prefix,
                Setting.prefix, Setting.prefix,
                Setting.prefix, Setting.prefix,
                Setting.prefix, Setting.prefix,
                Setting.prefix, Setting.prefix,
                Setting.prefix
            ), color=0x00ff00)
            embed.set_footer(text = "Ver. " + Setting.version + " | © 2018 Team. 화공")
            await app.send_message(message.author, embed=embed)
            await app.send_message(message.channel, "<@" + message.author.id + ">, DM으로 정보를 보냅니다!")
            if message.author.id == Setting.owner_id:
                embed = discord.Embed(title="서버 관리자 명령어!", description="%s익명로그 [#채널언급] - 익명을 사용하면 해당 채널에 로그가 남습니다!\n%s환영말 [할말 또는 끄기] - 할말을 적으면 해당 채널에 유저 입장시 환영말이 뜨며, 끄기를 적으면 비활성화 됩니다!\n%s나가는말 [할말 또는 끄기] - 할말을 적으면 해당 채널에 유저 퇴장시 떠나보내는말이 뜨며, 끄기를 적으면 비활성화 됩니다!" % (
                    Setting.prefix, Setting.prefix,
                    Setting.prefix
                ), color=0x00ff00)
                embed.set_footer(text = "Ver. " + Setting.version + " | © 2018 Team. 화공")
                await app.send_message(message.author, embed=embed)
                em = discord.Embed(title="Administrator commands!", description="%srtnotice [...] - Notice All Server!\n%srutap admin shutdown - shutdown!\n%srutap admin restart - restart!\n%srutap admin game - You can change Rutap Bot playing!" % (
                    Setting.prefix, Setting.prefix,
                    Setting.prefix, Setting.prefix
                ), color=0x00ff00)
                em.set_footer(text = "Ver. " + Setting.version + " | © 2018 Team. 화공")
                await app.send_message(message.author, embed=em)
            elif message.author.server_permissions.administrator:
                embed = discord.Embed(title="서버 관리자 명령어!", description="%s익명로그 [#채널언급] - 익명을 사용하면 해당 채널에 로그가 남습니다!\n%s환영말 [할말 또는 끄기] - 할말을 적으면 해당 채널에 유저 입장시 환영말이 뜨며, 끄기를 적으면 비활성화 됩니다!\n%s나가는말 [할말 또는 끄기] - 할말을 적으면 해당 채널에 유저 퇴장시 떠나보내는말이 뜨며, 끄기를 적으면 비활성화 됩니다!" % (
                    Setting.prefix, Setting.prefix,
                    Setting.prefix
                ), color=0x00ff00)
                embed.set_footer(text = "Ver. " + Setting.version + " | © 2018 Team. 화공")
                await app.send_message(message.author, embed=embed)
            else:
                return None
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    # 서버 관리자 명령어
    if message.content.startswith(Setting.prefix + '환영말'):
        try:
            if message.author.server_permissions.administrator:
                if message.content[5:].startswith('끄기'):
                    if os.path.isfile("%sServer_welcome_say_channel" % (
                        message.server.id
                    )):
                        os.remove("%sServer_welcome_say_channel" % (
                            message.server.id
                        ))
                        os.remove("%sServer_welcome_msg" % (
                            message.server.id
                        ))
                        embed = discord.Embed(title="완료!", description="앞으로 유저 입장시 환영말이 뜨지 않습니다!", color=0x00ff00)
                        embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                        await app.send_message(message.channel, embed=embed)
                    else:
                        await app.send_message(message.channel, "<@%s>, 설정한 환영말이 없습니다!" % (
                            message.author.id
                        ))
                else: 
                    welcome_msg = message.content[5:]
                    f = open("%sServer_welcome_say_channel" % (
                        message.server.id
                    ), 'w')
                    f.write(message.channel.id)
                    f.close()
                    f = open("%sServer_welcome_msg" % (
                        message.server.id
                    ), 'w')
                    f.write(welcome_msg)
                    f.close()
                    embed = discord.Embed(title="완료!", description="앞으로 이 채널에 환영말이 기록됩니다!\n\n설정한 환영말 : `(유저언급), %s`" % (
                        welcome_msg
                    ), color=0x00ff00)
                    embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                    await app.send_message(message.channel, embed=embed)
            else:
                await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (
                    message.author.id
                ))
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)
    
    if message.content.startswith(Setting.prefix + '나가는말'):
        try:
            if message.author.server_permissions.administrator:
                if message.content[6:].startswith('끄기'):
                    if os.path.isfile("%sServer_bye_say_channel" % (
                        message.server.id
                    )):
                        os.remove("%sServer_bye_say_channel" % (
                            message.server.id
                        ))
                        os.remove("%sServer_bye_msg" % (
                            message.server.id
                        ))
                        embed = discord.Embed(title="완료!", description="앞으로 유저 퇴장시 환영말이 뜨지 않습니다!", color=0x00ff00)
                        embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                        await app.send_message(message.channel, embed=embed)
                    else:
                        await app.send_message(message.channel, "<@%s>, 설정한 나가는말이 없습니다!" % (
                            message.author.id
                        ))
                else: 
                    bye_msg = message.content[6:]
                    f = open("%sServer_bye_say_channel" % (
                        message.server.id
                    ), 'w')
                    f.write(message.channel.id)
                    f.close()
                    f = open("%sServer_bye_msg" % (
                        message.server.id
                    ), 'w')
                    f.write(bye_msg)
                    f.close()
                    embed = discord.Embed(title="완료!", description="앞으로 이 채널에 나가는말이 기록됩니다!\n\n설정한 나가는말 : `(유저언급) %s`" % (
                        bye_msg
                    ), color=0x00ff00)
                    embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                    await app.send_message(message.channel, embed=embed)
            else:
                await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (
                    message.author.id
                ))
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if message.content.startswith(Setting.prefix + '익명로그'):
        try:
            if message.author.server_permissions.administrator:
                if message.content[6].startswith('<'):
                    channel_id = re.findall(r'\d+', message.content)
                    channel_id = channel_id[0]
                    channel_id = str(channel_id)
                    try:
                        await app.send_message(app.get_channel(channel_id), "Message Sending Test.")
                        f = open("%sServer_say_logging_channel" % (
                            message.server.id
                        ), 'w')
                        f.write(channel_id)
                        f.close()
                        embed = discord.Embed(title="완료!", description="앞으로 <#%s>채널에 익명 로그가 기록됩니다!" % (
                            channel_id
                        ), color=0x00ff00)
                        embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                        await app.send_message(message.channel, embed=embed)
                    except discord.HTTPException as er:
                        await app.send_message(message.channel, "<@%s>, 존재하는 채널을 입력해주세요!\n아니면, 봇이 채널에 메시지를 보내지 못할 수도 있습니다.\n\n```%s```" % (
                            message.author.id, er
                        ))
                else:
                   await app.send_message(message.channel, "<@%s>, 채널 언급을 제대로 해주세요! (채널 아이디 방식의 설정은 아직 지원하지 않습니다)" % (
                        message.author.id
                    )) 
            else:
                await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (
                    message.author.id
                ))
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    # 정보(그게 봇서버든 디코서버든 유저든 역할이든 상관 무)
    if Setting.prefix + "서버정보" == message.content:
        try:
            embed = discord.Embed(title="\"%s\" 서버정보!" % (
                message.server.name
            ), description="서버 소유자 : %s\n서버 생성일 : %s (UTC)\n서버 보안등급 : %s\n서버 위치 : %s\n\n서버 잠수채널 : `%s` (%s분 이상 잠수이면 이동됨)" % (
                message.server.owner, message.server.created_at,
                message.server.verification_level,message.server.region,
                message.server.afk_channel, message.server.afk_timeout/60
            ), color=0x00ff00)
            embed.set_image(url=message.server.icon_url)
            embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
            await app.send_message(message.channel, embed=embed)
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if message.content.startswith(Setting.prefix + '내정보'):
        try:
            userid = message.author.id
            embed = discord.Embed(title="\"%s\"의 정보!" % (
                message.author
            ), description="봇인가? : %s\n계정 생성일 : %s (UTC)\n서버 참가일 : %s (UTC)\n이 서버에서의 별칭 : %s" % (
                message.author.bot, message.author.created_at, message.author.joined_at, message.author.display_name
            ), color=0x00ff00)
            if message.author.avatar_url.startswith('https://'):
                embed.set_image(url=message.author.avatar_url)
                embed.set_footer(text = "User id : " + userid + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                await app.send_message(message.channel, embed=embed)
            else:
                embed.set_image(url=message.author.default_avatar_url)
                embed.set_footer(text = "User id : " + userid + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                await app.send_message(message.channel, embed=embed)
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if Setting.prefix + "정보" == message.content:
        try:
            embed = discord.Embed(title="About Rutap Bot!", description="\nTeam. 화공 공식 홈페이지 - ~~https://rutapofficial.xyz/~~ (홈페이지 DB 오류로 복구중)\nTeam. 루탑봇 소개\nhttps://about.rutapofficial.xyz/\n\n개발자 : 화향\n\n루탑봇은 오픈소스입니다! - https://github.com/hwahyang1/ru-top-bot-discord\n공식 서버가 존재합니다! 모든 공지와 초대링크는 공식 서버에 있습니다! - https://invite.gg/rutapbot\n\n또한, 본 봇은 메리(Mary)님의 `Discord-Python-Notice-Korean` 소스를 이용하여 공지를 돌리고 있습니다!\nhttps://github.com/kijk2869/Discord-Python-Notice-Korean" , color=0x00ff00)
            embed.set_footer(text = "Ver. " + Setting.version + " | © 2018 Team. 화공")
            await app.send_message(message.author, embed=embed)
            await app.send_message(message.channel, "<@" + message.author.id + ">, DM으로 정보를 보냅니다!")
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if Setting.prefix + "핑" == message.content:
        try:
            if os.path.isfile('no_ping.txt'):
                await app.send_message(message.channel, "<@" + message.author.id + ">,  서버의 안전을 위하여 상태를 한번에 여러명이 조회 할 수 없습니다!\n잠시 후 다시 시도 해 주세요!")
            else:
                now = datetime.datetime.now()

                f = open("no_ping.txt", 'w')
                f.close()

                send_time = message.timestamp.second * 100
                now_time = now.second * 100
                
                send_time_ms = message.timestamp.microsecond/1000
                now_time_ms = now.microsecond/1000

                st = int(send_time) + float(send_time_ms)
                nt = int(now_time) + float(now_time_ms)

                ping = nt - st

                if 0 < ping < 400:
                    embed = discord.Embed(title="루탑봇 상태!", description="서버 핑 : `" + str(ping) + "ms`(:large_blue_circle: 핑이 정상입니다.)\n\n봇 업타임  : https://status.hwahyang.xyz/", color=0x00ff00)
                    await app.send_message(message.channel, "<@" + message.author.id + ">, ", embed=embed)
                    os.remove("no_ping.txt")
                elif ping > 400:
                    embed = discord.Embed(title="루탑봇 상태!", description="서버 핑 : `" + str(ping) + "ms`(:red_circle: 핑이 비정상입니다.)\n\n봇 업타임  : https://status.hwahyang.xyz/", color=0x00ff00)
                    await app.send_message(message.channel, "<@" + message.author.id + ">, ", embed=embed)
                    os.remove("no_ping.txt")
                else:
                    embed = discord.Embed(title="루탑봇 상태!", description="서버 핑 : `" + str(ping) + "ms`(:question: 결과 도출 도중 알 수 없는 오류가 발생했습니다.)\n\n봇 업타임  : https://status.hwahyang.xyz/", color=0x00ff00)
                    await app.send_message(message.channel, "<@" + message.author.id + ">, ", embed=embed)
                    os.remove("no_ping.txt")
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)
            os.remove("no_ping.txt")

    if message.content == Setting.prefix + "시간":
        try:
            now = datetime.datetime.now()
            if now.hour > 12:
                hour = now.hour - 12
                embed = discord.Embed(title="현재 서버 시간은 %s년 %s월 %s일 오후 %s시 %s분 %s초 입니다!" % (
                    now.year, now.month,
                    now.day, hour,
                    now.minute, now.second
                ), description="", color=0x00ff00)
                embed.set_footer(text = "Seoul. (GMT +09:00) | Ver. " + Setting.version + " | © 2018 Team. 화공")
                await app.send_message(message.channel, embed=embed)
            else:
                embed = discord.Embed(title="현재 서버 시간은 %s년 %s월 %s일 오전 %s시 %s분 %s초 입니다!" % (
                    now.year, now.month,
                    now.day, now.hour,
                    now.minute, now.second
                ), description="", color=0x00ff00)
                embed.set_footer(text = "Seoul. (GMT +09:00) | Ver. " + Setting.version + " | © 2018 Team. 화공")
                await app.send_message(message.channel, embed=embed)
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    # afk
    if message.content.startswith(Setting.prefix + '잠수'): 

        if os.path.isfile("afk" + message.author.id + ".txt"):
            return None
        else:
            try:
                now = datetime.datetime.now()

                imafk = message.content[4:]

                f = open("afk_year" + message.author.id + ".txt", 'w')
                f.write(str(now.year))
                f.close()

                f = open("afk_month" + message.author.id + ".txt", 'w')
                f.write(str(now.month))
                f.close()

                f = open("afk_day" + message.author.id + ".txt", 'w')
                f.write(str(now.day))
                f.close()

                f = open("afk_hour" + message.author.id + ".txt", 'w')
                f.write(str(now.hour))
                f.close()

                f = open("afk_min" + message.author.id + ".txt", 'w')
                f.write(str(now.minute))
                f.close()

                f = open("afk_because" + message.author.id + ".txt", 'w')
                f.write(imafk)
                f.close()

                embed = discord.Embed(title="잠수시작!", description="USER : <@" + message.author.id + ">\n\n잠수 시작 시간 : " + str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 " + str(now.hour) + "시 " + str(now.minute) + "분\n\n사유 : " + imafk + "", color=0x00ff00)
                await app.send_message(message.channel, embed=embed)
            except Exception as er:
                embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
                embed.set_footer(text = er)
                await app.send_message(message.author, embed=embed)

    if message.content.startswith('<@') or message.content.endswith('>'):
        try: 
            if int(message.author.id) == int(app.user.id):
                return None
            else:
                mention_id = re.findall(r'\d+', message.content)
                mention_id = mention_id[0]
                mention_id = str(mention_id)
                if os.path.isfile("afk_because" + mention_id + ".txt"):
                    f = open("afk_year" + mention_id + ".txt", 'r')
                    year = f.read()
                    f.close()
                    f = open("afk_month" + mention_id + ".txt", 'r')
                    month = f.read()
                    f.close()
                    f = open("afk_day" + mention_id + ".txt", 'r')
                    day = f.read()
                    f.close()
                    f = open("afk_hour" + mention_id + ".txt", 'r')
                    hour = f.read()
                    f.close()
                    f = open("afk_min" + mention_id + ".txt", 'r')
                    minute = f.read()
                    f.close()
                    f = open("afk_because" + mention_id + ".txt", 'r')
                    imafk = f.read()
                    f.close()
                    embed = discord.Embed(title="잠수 상태!", description="USER : <@" + mention_id + ">\n\n잠수 시작 시간 : " + str(year) + "년 " + str(month) + "월 " + str(day) + "일 " + str(hour) + "시 " + str(minute) + "분\n\n사유 : " + imafk + "", color=0x00ff00)
                    await app.send_message(message.channel,"<@" + message.author.id + ">, \n<@" + mention_id +">님은 현재 잠수 중 입니다!" ,embed=embed)
                else:
                    return None
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    # Google 이미지 보내기
    if Setting.prefix + "이미지" == message.content.split(" ")[0]:
        try:
            group = message.content[5:]

            google_data = requests.get("https://www.google.co.kr/search?q=" + group + "&dcr=0&source=lnms&tbm=isch&sa=X")
            soup = bs(google_data.text, "html.parser")
            imgs = soup.find_all("img")

            embed = discord.Embed(title="", description="", color=0x00d8ff)
            embed.set_image(url=random.choice(imgs[1:])['src'])
            await app.send_message(message.channel, "<@" + message.author.id + ">, `%s`에 대한 검색 결과 :\n\n" % (
                message.content[5:]
            ), embed=embed)

            del group, google_data, soup, imgs
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if Setting.prefix + "익명" == message.content.split(" ")[0]:
        
        try:
            f = open("non-del.txt", 'w')
            f.close()

            global bot_deleting

            msg = " ".join(message.content.split(" ")[1:])
            channel = message.channel

            bot_deleting = True
            await app.delete_message(message)
            bot_deleting = False

            await app.send_message(channel, msg)
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)
            os.remove("non-del.txt")

    # 경고
    if message.content == Setting.prefix + "경고":
        try:
            embed = discord.Embed(title="경고관련 명령어!", description="%s경고 확인 - 당신이 받은 경고 횟수를 확인합니다. 명령어 뒤에 멘션을 하여 특정 유저의 경고 상태를 볼 수 있습니다.\n%s경고 부여 [멘션]  - 경고를 부여합니다. 관리자 권한을 보유하고 있어야 가능합니다.\n%s경고 제거 [멘션]  - 경고를 제거합니다. 관리자 권한을 보유하고 있어야 가능합니다.\n%s경고 초기화 [멘션]  - 경고를 초기화합니다. 관리자 권한을 보유하고 있어야 가능합니다.\n\n일부 구문은 `The_Adminator#4074`님께서 제공 해 주셨습니다." % (
                Setting.prefix, Setting.prefix, Setting.prefix, Setting.prefix
            ), color=0x00ff00)
            embed.set_footer(text = "Ver. " + Setting.version + " | Server id : " + message.server.id + " | © 2018 Team. 화공")
            await app.send_message(message.channel, embed=embed)
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if message.content.startswith('/경고 확인'):
        try:
            await app.send_message(message.channel, "<@" + message.author.id + ">, Ver. " + Setting.version + "")
            await app.send_message(message.channel, "<@" + message.author.id + ">, Command Check Success!")
            if message.content[7:].startswith('<'):
                await app.send_message(message.channel, "<@" + message.author.id + ">, Command Startswith \"<\"!")
                mention_id = re.findall(r'\d+', message.content)
                mention_id = mention_id[0]
                mention_id = str(mention_id)
                await app.send_message(message.channel, "<@" + message.author.id + ">, Usr ID : " + mention_id + "")
                if os.path.isfile("warn_server" + message.server.id + "_user_" + mention_id + ".txt"):
                    f = open("warn_server" + message.server.id + "_user_" + mention_id + ".txt", 'r')
                    warn_num = f.read()
                    f.close()
                    embed = discord.Embed(title="경고 스탯!", description="대상 유저 : <@" + mention_id + ">\n이 서버에서 경고를 " + warn_num + "회 받았습니다.", color=0x00ff00)
                    embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                    await app.send_message(message.channel, embed=embed)
                else:
                    embed = discord.Embed(title="경고 스탯!", description="대상 유저 : <@" + mention_id + ">\n이 서버에서 경고를 받은 적이 없습니다.", color=0x00ff00)
                    embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                    await app.send_message(message.channel, embed=embed)
            else:
                await app.send_message(message.channel, "<@" + message.author.id + ">, Command No Startswith \"<\"!")
                await app.send_message(message.channel, "<@" + message.author.id + ">, message content : `" + message.content + "`")
                mention_id = message.author.id
                if os.path.isfile("warn_server" + message.server.id + "_user_" + message.author.id + ".txt"):
                    f = open("warn_server" + message.server.id + "_user_" + message.author.id + ".txt", 'r')
                    warn_num = f.read()
                    f.close()
                    embed = discord.Embed(title="경고 스탯!", description="대상 유저 : <@" + mention_id + ">\n이 서버에서 경고를 " + warn_num + "회 받았습니다.", color=0x00ff00)
                    embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                    await app.send_message(message.channel, embed=embed)
                else:
                    embed = discord.Embed(title="경고 스탯!", description="대상 유저 : <@" + mention_id + ">\n이 서버에서 경고를 받은 적이 없습니다.", color=0x00ff00)
                    embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                    await app.send_message(message.channel, embed=embed)
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if message.content.startswith('/경고 부여'):
        try:
            await app.send_message(message.channel, "<@" + message.author.id + ">, Ver. " + Setting.version + "")
            await app.send_message(message.channel, "<@" + message.author.id + ">, Command Check Success!")
            if message.author.server_permissions.administrator:
                # 관리자 권한이 있는 경우에 해당됩니다.
                if message.content[7:].startswith('<'):
                    await app.send_message(message.channel, "<@" + message.author.id + ">, Command Startswith \"<\"!")
                    mention_id = re.findall(r'\d+', message.content)
                    mention_id = mention_id[0]
                    mention_id = str(mention_id)
                    if os.path.isfile("warn_server" + message.server.id + "_user_" + mention_id + ".txt"):
                        await app.send_message(message.channel, "<@" + message.author.id + ">, `warn_server" + message.server.id + "_user_" + mention_id + ".txt` Check Success!")
                        # 이사람이 경고를 받은 적이 경우에 해당됩니다.
                        f = open("warn_server" + message.server.id + "_user_" + mention_id + ".txt", 'r')
                        past_warn = f.read()
                        f.close()
                        now_warn = int(past_warn) + int(1)
                        now_warn = str(now_warn)
                        f = open("warn_server" + message.server.id + "_user_" + mention_id + ".txt", 'w')
                        f.write(now_warn)
                        f.close()
                        await app.send_message(message.channel, "<@" + message.author.id + ">, Success!")
                        embed = discord.Embed(title="경고가 발생했습니다!", description="관리자 : <@" + message.author.id + ">\n대상 유저 : <@" + mention_id + ">\n총 경고 : " + now_warn + "", color=0x00ff00)
                        embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                        await app.send_message(app.get_channel("463719199441944577"), embed=embed)
                    else:
                        # 이사람이 경고를 받은 적이 없는 경우에 해당됩니다.
                        await app.send_message(message.channel, "<@" + message.author.id + ">, `warn_server" + message.server.id + "_user_" + mention_id + ".txt` Check Success!")
                        f = open("warn_server" + message.server.id + "_user_" + mention_id + ".txt", 'w')
                        f.write(str(1))
                        f.close()
                        await app.send_message(message.channel, "<@" + message.author.id + ">, Success!")
                        embed = discord.Embed(title="경고가 발생했습니다!", description="관리자 : <@" + message.author.id + ">\n대상 유저 : <@" + mention_id + ">\n총 경고 : " + str(1) + "", color=0x00ff00)
                        embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                        await app.send_message(app.get_channel("463719199441944577"), embed=embed)
                else:
                    embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
                    embed.set_footer(text = "유저를 언급해야 합니다!")
                    await app.send_message(message.author, embed=embed)
            else:
                # 관리자 권한이 없는 경우에 해당됩니다.
                embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
                embed.set_footer(text = "당신은 관리자 권한이 없습니다!")
                await app.send_message(message.author, embed=embed)
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if message.content.startswith('/경고 제거'):
        try:
            await app.send_message(message.channel, "<@" + message.author.id + ">, Ver. " + Setting.version + "")
            await app.send_message(message.channel, "<@" + message.author.id + ">, Command Check Success!")
            if message.author.server_permissions.administrator:
                # 관리자 권한이 있는 경우에 해당됩니다.
                if message.content[7:].startswith('<'):
                    await app.send_message(message.channel, "<@" + message.author.id + ">, Command Startswith \"<\"!")
                    mention_id = re.findall(r'\d+', message.content)
                    mention_id = mention_id[0]
                    mention_id = str(mention_id)
                    if os.path.isfile("warn_server" + message.server.id + "_user_" + mention_id + ".txt"):
                        await app.send_message(message.channel, "<@" + message.author.id + ">, `warn_server" + message.server.id + "_user_" + mention_id + ".txt` Check Success!")
                        # 이사람이 경고를 받은 적이 경우에 해당됩니다.
                        f = open("warn_server" + message.server.id + "_user_" + mention_id + ".txt", 'r')
                        past_warn = f.read()
                        f.close()
                        now_warn = int(past_warn) - int(1)
                        now_warn = str(now_warn)
                        f = open("warn_server" + message.server.id + "_user_" + mention_id + ".txt", 'w')
                        f.write(now_warn)
                        f.close()
                        await app.send_message(message.channel, "<@" + message.author.id + ">, Success!")
                        embed = discord.Embed(title="경고 철회가 발생했습니다!", description="관리자 : <@" + message.author.id + ">\n대상 유저 : <@" + mention_id + ">\n총 경고 : " + now_warn + "", color=0x00ff00)
                        embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                        await app.send_message(app.get_channel("463719199441944577"), embed=embed)
                    else:
                        # 이사람이 경고를 받은 적이 없는 경우에 해당됩니다.
                        await app.send_message(message.channel, "<@" + message.author.id + ">, Success!")
                        embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
                        embed.set_footer(text = "대상 유저는 경고를 보유하고 있지 않습니다!")
                        await app.send_message(message.author, embed=embed)
                else:
                    embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
                    embed.set_footer(text = "유저를 언급해야 합니다!")
                    await app.send_message(message.author, embed=embed)
            else:
                # 관리자 권한이 없는 경우에 해당됩니다.
                embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
                embed.set_footer(text = "당신은 관리자 권한이 없습니다!")
                await app.send_message(message.author, embed=embed)
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if message.content.startswith('/경고 초기화'):
        try:
            await app.send_message(message.channel, "<@" + message.author.id + ">, Ver. " + Setting.version + "")
            await app.send_message(message.channel, "<@" + message.author.id + ">, Command Check Success!")
            if message.author.server_permissions.administrator:
                # 관리자 권한이 있는 경우에 해당됩니다.
                if message.content[8:].startswith('<'):
                    await app.send_message(message.channel, "<@" + message.author.id + ">, Command Startswith \"<\"!")
                    mention_id = re.findall(r'\d+', message.content)
                    mention_id = mention_id[0]
                    mention_id = str(mention_id)
                    if os.path.isfile("warn_server" + message.server.id + "_user_" + mention_id + ".txt"):
                        await app.send_message(message.channel, "<@" + message.author.id + ">, `warn_server" + message.server.id + "_user_" + mention_id + ".txt` Check Success!")
                        # 이사람이 경고를 받은 적이 경우에 해당됩니다.
                        os.remove("warn_server" + message.server.id + "_user_" + mention_id + ".txt")
                        await app.send_message(message.channel, "<@" + message.author.id + ">, Success!")
                        embed = discord.Embed(title="경고 초기화가 발생했습니다!", description="관리자 : <@" + message.author.id + ">\n대상 유저 : <@" + mention_id + ">", color=0x00ff00)
                        embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
                        await app.send_message(app.get_channel("463719199441944577"), embed=embed)
                    else:
                        # 이사람이 경고를 받은 적이 없는 경우에 해당됩니다.
                        embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
                        embed.set_footer(text = "대상 유저는 경고를 보유하고 있지 않습니다!")
                        await app.send_message(message.author, embed=embed)
                else:
                    embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
                    embed.set_footer(text = "유저를 언급해야 합니다!")
                    await app.send_message(message.author, embed=embed)
            else:
                embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
                embed.set_footer(text = "당신은 관리자가 아닙니다!")
                await app.send_message(message.author, embed=embed)
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if message.content.startswith(Setting.prefix + '지우기'):
        try:
            if message.author.server_permissions.administrator:
                if int(0) < int(message.content[5:]):
                    
                    await app.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), title="모듈 초기화중..."))

                    cleared = -2
                    failed = 0

                    await asyncio.sleep(random.choice(range(0,2)))

                    async for m in app.logs_from(message.channel, limit=int(message.content[5:]) + int(2)):
                        try:
                            await app.delete_message(m)
                            cleared += 1
                        except:
                            failed += 1
                            pass

                    if failed == 0:
                        returnmsg = await app.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), title="%s개의 메세지를 삭제하였으며, 0개의 메시지를 삭제하지 못하였습니다." % (
                            cleared
                        ), description=""))
                        await asyncio.sleep(10)
                        await app.delete_message(returnmsg)
                    else:
                        returnmsg = await app.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), title="%s개의 메세지를 삭제하였으며, %s개의 메시지를 삭제하지 못하였습니다." % (
                            cleared, failed
                        ), description="(추정 원인 : 메시지 관리 권한이 없거나, 너무 오래된 메시지 입니다)"))
                        await asyncio.sleep(5)
                        await app.delete_message(returnmsg)
                else:
                    await app.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), title="지울 만큼의 메세지 수를 제대로 적어주세요!"))
            else:
                await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (
                    message.author.id
                ))
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

    if message.content.startswith(Setting.prefix + "투표"):
        try:
            await app.send_message(message.channel, "<@%s>, 점검중입니다!" % (
                message.author.id
            ))
        except Exception as er:
            embed = discord.Embed(title="애러가 발생했습니다!", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주세요!\nhttps://invite.gg/rutapbot", color=0x00ff00)
            embed.set_footer(text = er)
            await app.send_message(message.author, embed=embed)

app.run(Setting.token)
