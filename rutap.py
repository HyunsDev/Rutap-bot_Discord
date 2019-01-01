# -*- coding: utf-8 -*- 

##########################################################
#                Rutap Bot 2019 Main Module              #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
#             GNU General Public License v3.0            #
##########################################################

import asyncio, discord, os, requests, random, datetime, re, json, sys, time, setting
from activity_log import log_actvity, log_start_actvity
from msg_log import log_msg, log_start_msg
from preta import timeform
from bs4 import BeautifulSoup as bs4

Setting = setting.Settings()
Copyright = Setting.copy
app = discord.Client()
now = datetime.datetime.now()
a = 0

@app.event
async def on_ready():
    try:
        rpc = open("rpc.rts", 'r').read()
        print("rpc.rts 파일을 발견하였습니다.\n봇이 \"%s\" 을(를) 플레이 하게 됩니다.\n\n==============\n" % (rpc))
        await app.change_presence(game=discord.Game(name=rpc, type=0))
    except FileNotFoundError as e:
        print("rpc.rts 파일을 발견하지 못하였습니다.\n봇이 아무것도 플레이하지 않게 됩니다.\n\n애러 내용 : \"%s\"\n\n==============\n" % (e))

    print("Bot is Ready!\n\n==============\n\n= Rutap Bot 2019 Main Module =\n\n[로그인 정보]\n봇 이름 : %s\n봇 ID : %s\n\n[설정 정보]\n기본 접두사 : %s\n봇 관리자 ID : %s\n로그 파일 저장위치 : log/%s\n봇 활동로그 저장위치 : log/%s\n봇 온라인 알림 메시지 전송 채널 : %s(%s)\n봇 버전 : %s\n\n%s. All Rights Reserved.\nGNU General Public License v3.0\n\n==============\n" % (app.user.name, app.user.id, Setting.prefix, Setting.owner_id, Setting.log_file, Setting.actvity_log_file, Setting.online_notice_channel, app.get_channel(Setting.online_notice_channel), Setting.version, Copyright))
    
    log_start_msg()
    log_start_actvity()

    count = 1

    embed=discord.Embed(title="I'm online!", color=0xb2ebf4)
    embed.add_field(name="Last Checked in", value="`%s/%s/%s` | `%s:%s:%s` | `%s차`" % (now.year, now.month, now.day, now.hour, now.minute, now.second, count), inline=True)
    embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
    online_notice = await app.send_message(app.get_channel(Setting.online_notice_channel), embed=embed)

    while a < 1:
        await asyncio.sleep(300)
        count = count + 1
        snow = datetime.datetime.now()
        embed=discord.Embed(title="I'm online!", color=0xb2ebf4)
        embed.add_field(name="Last Checked in", value="`%s/%s/%s` | `%s:%s:%s` | `%s차`" % (snow.year, snow.month, snow.day, snow.hour, snow.minute, snow.second, count), inline=True)
        embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
        await app.edit_message(online_notice, embed=embed)

@app.event
async def on_member_join(member):
    log_actvity("%s joined in %s!" % (member.id, member.server.id))
    if os.path.isfile("Server_%s/%sServer_welcome_say_channel.rts" % (member.server.id, member.server.id)):
        message_server = open("Server_%s/%sServer_welcome_say_channel.rts" % (member.server.id, member.server.id), 'r').read()
        welcome_msg = open("Server_%s/%sServer_welcome_msg.rts" % (member.server.id, member.server.id), 'r').read()
        await app.send_message(app.get_channel(message_server), "<@%s>, %s" % (member.id, welcome_msg))
    else:
        return None

@app.event
async def on_member_remove(member):
    log_actvity("%s has left %s!" % (member.id, member.server.id))
    if os.path.isfile("Server_%s/%sServer_bye_say_channel.rts" % (member.server.id, member.server.id)):
        message_server = open("Server_%s/%sServer_bye_say_channel.rts" % (member.server.id, member.server.id), 'r').read()
        bye_msg = open("Server_%s/%sServer_bye_msg.rts" % (member.server.id, member.server.id), 'r').read()
        await app.send_message(app.get_channel(message_server), "`%s%s`, %s" % (member.name, "#"+member.discriminator, bye_msg))
    else:
        return None

@app.event
async def on_message(message):
    try:
        try:
            log_msg(message.server, message.server.id, message.channel, message.channel.id, message.author.name, "#"+message.author.discriminator, message.author.id, message.content)


            if message.author.bot or os.path.isfile("%s_Banned.rts" % (message.author.id)) or message.author.id == app.user.id:
                return None
                
            if os.path.isfile("Server_%s/%s_Server_prefix.rts" % (message.server.id, message.server.id)):
                prefix = open("Server_%s/%s_Server_prefix.rts" % (message.server.id, message.server.id), 'r').read()

                if os.path.isfile("afk/afk_because%s.rtl" % (message.author.id)):

                    past_year = open("afk/afk_year%s.rtl" % (message.author.id), 'r').read()
                    past_month = open("afk/afk_month%s.rtl" % (message.author.id), 'r').read()
                    past_day = open("afk/afk_day%s.rtl" % (message.author.id), 'r').read()
                    past_hour = open("afk/afk_hour%s.rtl" % (message.author.id), 'r').read()
                    past_min = open("afk/afk_min%s.rtl" % (message.author.id), 'r').read()
                    imafk = open("afk/afk_because%s.rtl" % (message.author.id), 'r').read()

                    os.remove("afk/afk_year%s.rtl" % (message.author.id))
                    os.remove("afk/afk_month%s.rtl" % (message.author.id))
                    os.remove("afk/afk_day%s.rtl" % (message.author.id))
                    os.remove("afk/afk_hour%s.rtl" % (message.author.id))
                    os.remove("afk/afk_min%s.rtl" % (message.author.id))
                    os.remove("afk/afk_because%s.rtl" % (message.author.id))

                    embed = discord.Embed(title="잠수종료!", description=None, color=0xb2ebf4)
                    embed.add_field(name="대상 유저", value="<@%s>" % (message.author.id), inline=False)
                    embed.add_field(name="사유", value=imafk, inline=False)
                    embed.add_field(name="잠수 시작 시간", value="%s/%s/%s | %s:%s" % (str(past_year), str(past_month), str(past_day), str(past_hour), str(past_min)), inline=True)
                    embed.add_field(name="잠수 종료 시간", value="%s/%s/%s | %s:%s" % (str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute)), inline=True)
                    embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                    await app.send_message(message.channel, embed=embed)
                    log_actvity("AFK of %s has ended" % (message.author.id))

                if "rutap admin shutdown" == message.content:
                    if message.author.id == Setting.owner_id:
                        await app.send_message(message.channel, "<@%s>, 봇의 가동을 중지합니다. 5분 이내로 오프라인으로 전환됩니다(디스코드 API 딜레이)." % (message.author.id))
                        await app.change_presence(game=discord.Game(name="Offline", type=0))
                        log_actvity("Change status to offline (Request by. %s)." % (message.author.id))
                        quit() # 왜왜애왜 애러나
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))

                if message.content.startswith('rutap admin game'):
                    if message.author.id == Setting.owner_id:
                        playing = message.content[17:]
                        if playing == "":
                            await app.send_message(message.channel, "<@%s>, 게임명은 비워둘 수 없습니다. 다시 시도 해 주세요." % (message.author.id))
                        else:
                            await app.send_message(message.channel, "<@%s>, 봇이 `%s`을(를) 플레이 하게 됩니다." % (message.author.id, playing))
                            await app.change_presence(game=discord.Game(name=playing, type=0))
                            log_actvity("Change rpc to %s (Request by. %s)." % (playing, message.author.id))
                            f = open("rpc.rts", 'w')
                            f.write(playing)
                            f.close()
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))

                if message.content.startswith('rutap admin ban'):
                    if message.author.id == Setting.owner_id:
                        q = message.content[16:]
                        if q == message.author.id:
                            open("%s_Banned.rts" % (q), 'w').close()
                            await app.send_message(message.channel, "<@%s>, 앞으로 `%s`님의 모든 메시지를 무시합니다." % (message.author.id, q))
                            log_actvity("I'll Ban %s. (Request by. %s)." % (q, message.author.id))
                        else:
                            await app.send_message(message.channel, "<@%s>, 자기 자신을 밴 시킬 수 없습니다!" % (message.author.id))
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))

                if message.content.startswith('rutap admin unban'):
                    if message.author.id == Setting.owner_id:
                        q = message.content[16:]
                        if os.path.isfile("%s_Banned.rts" % (q)):
                            os.remove("%s_Banned.rts" % (q), 'w')
                            await app.send_message(message.channel, "<@%s>, 앞으로 `%s`님의 모든 메시지를 무시하지 않습니다." % (message.author.id, q))
                            log_actvity("I'll UnBan %s. (Request by. %s)." % (q, message.author.id))
                        else:
                            await app.send_message(message.channel, "<@%s>, 해당 유저는 밴 되지 않았습니다!" % (message.author.id))
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))

                if message.content.startswith('rutap admin debug'):
                    if message.content == "rutap admin debug help":
                        embed = discord.Embed(title="Command of debug Category!", description="`rutap admin debug prefix`\n`rutap admin debug file -r(-d) [filename]`\n`rutap admin debug ping`", color=0xb2ebf4)
                        embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                    elif message.content == "rutap admin debug prefix":
                        if message.author.id == Setting.owner_id:
                            await app.send_message(message.channel, "<@%s>, `%s` 서버에서의 접두사는 `%s` 입니다!" % (message.author.id, prefix, message.server.name))
                        else:
                            await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))
                    elif message.content.startswith('rutap admin debug file -r'):
                        if message.author.id == Setting.owner_id:
                            q = message.content[26:]
                            try:
                                content = open(q, 'r').read()
                                await app.send_message(message.channel, "<@%s>, `%s` 파일의 내용입니다 : \n```%s```" % (message.author.id, q, content))
                            except Exception as e:
                                await app.send_message(message.channel, "<@%s>, 문제가 발생하였습니다.\n\n```%s```" % (message.author.id, e))
                        else:
                            await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))
                    elif message.content.startswith('rutap admin debug file -d'):
                        if message.author.id == Setting.owner_id:
                            q = message.content[26:]
                            try:
                                os.remove(q)
                                await app.send_message(message.channel, "<@%s>, 성공적으로 `%s`을(를) 삭제하였습니다." % (message.author.id, q))
                            except Exception as e:
                                await app.send_message(message.channel, "<@%s>, 문제가 발생하였습니다.\n\n```%s```" % (message.author.id, e))
                        else:
                            await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))
                    elif message.content == "rutap admin debug ping":
                        if message.author.id == Setting.owner_id:
                            msgarrived = float(str(time.time())[:-3])
                            msgtime = timeform(message.timestamp)
                            msgdelay = msgarrived - msgtime - 32400
                            pong = int(msgdelay * 1000)
                            await app.send_message(message.channel, "<@%s>,\nmsgarrived : `%s`\nmsgtime : `%s`\nmsgdelay : `%s`\nping : `%sms`" % (message.author.id, msgarrived, msgtime, msgdelay, pong))
                        else:
                            await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))
                    else:
                        return None

                if "rutap admin notice -s all" in message.content:
                    if message.author.id == Setting.owner_id:
                        # DPNK 사용 구문 시점
                        embed=discord.Embed(title="루탑봇 전체공지 시스템", color=0xb2ebf4)
                        embed.add_field(name="공지 발신을 준비하고 있습니다!", value="요청자 : <@" + message.author.id + ">", inline=True)
                        embed.set_footer(text = "Module by. Mary | Ver. %s | %s" % (Setting.version, Copyright))
                        mssg = await app.send_message(message.channel, embed=embed)
                        a = []
                        b = []
                        e = []
                        ec = {}
                        embed=discord.Embed(title="루탑봇 전체공지 시스템", color=0xb2ebf4)
                        embed.add_field(name="공지 발신중 입니다!", value="요청자 : <@" + message.author.id + ">", inline=True)
                        embed.set_footer(text = "Module by. Mary | Ver. %s | %s" % (Setting.version, Copyright))
                        await app.edit_message(mssg, embed=embed)
                        for server in app.servers:
                            for channel in server.channels:
                                for tag in ["notice", "공지", "알림", "Alarm"]:
                                    if tag in channel.name:
                                        dtat = True
                                        for distag in ["밴", "경고", "제재", "길드", "ban", "worry", "warn", "guild"]:
                                            if distag in channel.name:
                                                dtat = False
                                        if dtat:
                                            if not server.id in a:
                                                try:
                                                    await app.send_message(channel, message.content)
                                                except discord.HTTPException:
                                                    e.append(str(channel.id))
                                                    ec[channel.id] = "HTTPException"
                                                except discord.Forbidden:
                                                    e.append(str(channel.id))
                                                    ec[channel.id] = "Forbidden"
                                                except discord.NotFound:
                                                    e.append(str(channel.id))
                                                    ec[channel.id] = "NotFound"
                                                except discord.InvalidArgument:
                                                    e.append(str(channel.id))
                                                    ec[channel.id] = "InvalidArgument"
                                                else:
                                                    a.append(str(server.id))
                                                    b.append(str(channel.id))
                        asdf = "```\n"
                        for server in app.servers:
                            if not server.id in a:
                                try:
                                    ch = await app.create_channel(server, "Team-화공-공지-자동생성됨")
                                    await app.send_message(ch, "**__공지 채널을 발견하지 못하여 자동적으로 해당 채널을 생성하였습니다.__**\n자세한 사항은 루탑봇 지원 서버나 팀장 DM으로 부탁드립니다.\n\n지원 서버 : https://invite.gg/rutapbot\nDiscord : HwaHyang - Official#4037")
                                    await app.send_message(ch, message.content)
                                except:
                                    asdf = asdf + str(server.name) + "[채널 생성에 실패하였습니다. (서버 관리자와 연락 요망)]\n"
                                else:
                                    asdf = asdf + str(server.name) + "[채널 생성 및 재발송에 성공하였습니다.]\n"
                        asdf = asdf + "```"
                        embed=discord.Embed(title="루탑봇 전체공지 시스템", color=0xb2ebf4)
                        embed.add_field(name="공지 발신이 완료되었습니다!", value="요청자 : <@" + message.author.id + ">", inline=True)
                        bs = "```\n"
                        es = "```\n"
                        for bf in b:
                            bn = app.get_channel(bf).name
                            bs = bs + str(bn) + "\n"
                        for ef in e:
                            en = app.get_channel(ef).name
                            es = es + str(app.get_channel(ef).server.name) + "(#" + str(en) + ") : " + ec[ef] + "\n"
                        bs = bs + "```"
                        es = es + "```"
                        if bs == "``````":
                            bs = "``` ```"
                        if es == "``````":
                            es = "``` ```"
                        if asdf == "``````":
                            asdf = "``` ```"
                        sucess = bs
                        missing = es
                        notfound = asdf
                        embed.add_field(name="공지 발신에 성공한 채널은 다음과 같습니다 :", value=sucess, inline=False)
                        embed.add_field(name="공지 발신에 실패한 채널은 다음과 같습니다 :", value=missing, inline=False)
                        embed.add_field(name="키워드가 발견되지 않은 서버는 다음과 같습니다 :", value=notfound, inline=False)
                        embed.set_footer(text = "Module by. Mary | Ver. %s | %s" % (Setting.version, Copyright))
                        await app.edit_message(mssg, embed=embed)
                        # DPNK 사용 구문 종점
                        log_actvity("I send Notice for all Server. (content : %s\nSuccess : %s\nFail : %s\nNotfound : %s)." % (message.content, sucess, missing, notfound))
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))

                if "rutap admin notice -s set" in message.content:
                    if message.author.id == Setting.owner_id:
                        f = open("notice_memo.rts", 'w')
                        f.write(message.content)
                        f.close()
                        await app.send_message(message.channel, "<@%s>, 공지 내용을 성공적으로 등록하였습니다!\n`rutap admin notice -s channel [id]`를 입력하여 공지를 보낼 수 있습니다." % (message.author.id))
                        log_actvity("I set Notice memo. (Content : %s)." % (message.content))
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))

                if message.content.startswith('rutap admin notice -s channel'):
                    if message.author.id == Setting.owner_id:
                        q = open("notice_memo.rts", 'r').read()
                        q_channel = message.content[30:]
                        channel_info = app.get_channel(q_channel)
                        try:
                            await app.send_message(channel_info, q)
                            await app.send_message(message.channel, "<@%s>, 성공적으로 `%s`에 메시지를 보냈습니다!" % (message.author.id, channel_info))
                            log_actvity("I send Notice for %s(%s)." % (q_channel, channel_info))
                        except Exception as e:
                            await app.send_message(message.channel, "<@%s>, `%s`에 메시지를 보내지 못하였습니다.\n\n```%s```" % (message.author.id, channel_info, e))
                            log_actvity("I Failed to send Notice for %s(%s). : %s" % (q_channel, channel_info, e))
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))

                if os.path.isfile("Server_%s/%s_Server_CC_%s.rts" % (message.server.id, message.server.id, message.content[1:])):
                    response = open("Server_%s/%s_Server_CC_%s.rts" % (message.server.id, message.server.id, message.content[1:])).read()
                    embed = discord.Embed(title=None, description=response, color=0xb2ebf4)
                    embed.set_footer(text = "\'%sCC 제거\'를 통해 제거가 가능합니다! | Ver. %s | %s" % (prefix, Setting.version, Copyright))
                    await app.send_message(message.channel, embed=embed)

                if message.content == prefix + "도움말":
                    embed = discord.Embed(title="루탑봇 명령어!", description=None, color=0xb2ebf4)
                    embed.add_field(name="봇 관련 명령어!", value="`%s도움말` - 봇의 명령어를 출력합니다. `%s도움말 전체` 를 입력하여 모든 명령어를 볼 수 있습니다.\n`%s정보` - 봇의 정보를 출력합니다!" % (prefix, prefix, prefix), inline=False)
                    embed.add_field(name="봇 서버 관련 명령어!", value="`%s핑` - 현재 봇 서버의 응답속도를 확인합니다.\n`%s시간` - 현재 시간을 서버에서 가져옵니다." % (prefix, prefix), inline=False)
                    embed.add_field(name="정보 관련 명령어!", value="`%s서버정보` - 서버의 정보를 불러옵니다.\n|     아직은 노출할 수 있는 정보가 별로 없지만, 추후 지속적인 업데이트를 통하여 노출되는 정보를 추가할 예정입니다." % (prefix), inline=False)
                    embed.add_field(name="편의 관련 명령어!", value="`%s잠수 [사유]` - 잠수모드에 진입합니다. 타인이 자신을 언급하면 잠수중이라는 알림을 보냅니다.\n`%s이미지 [검색어]` - 구글에서 랜덤으로 사진 한장을 가져옵니다.\n`%s지우기 [숫자]` - 특정한 갯수의 메시지를 지울 수 있습니다!\n`%s냥이` - 랜덤으로 냥이 짤을 불러옵니다." % (prefix, prefix, prefix, prefix), inline=False)
                    embed.add_field(name="경고 관련 명령어!", value="`%s경고 확인` - 당신이 받은 경고 횟수를 확인합니다. 명령어 뒤에 멘션을 하여 특정 유저의 경고 상태를 볼 수 있습니다.\n`%s경고 부여 [멘션]`  - 경고를 부여합니다. 관리자 권한을 보유하고 있어야 가능합니다.\n`%s경고 제거 [멘션]`  - 경고를 제거합니다. 관리자 권한을 보유하고 있어야 가능합니다.\n`%s경고 초기화 [멘션]`  - 경고를 초기화합니다. 관리자 권한을 보유하고 있어야 가능합니다." % (prefix, prefix, prefix, prefix), inline=False)
                    if message.author.id == Setting.owner_id:
                        embed.add_field(name="서버 관리자 명령어!", value="`%sCC 추가 [원하는 명령어]` - 커스텀 커맨드(이하 CC)를 만들 수 있습니다. 서버당 5개 제한이 있습니다.\n`%s환영말 [할말 또는 끄기]` - 할말을 적으면 해당 채널에 유저 입장시 환영말이 뜨며, 끄기를 적으면 비활성화 됩니다!\n`%s나가는말 [할말 또는 끄기]` - 할말을 적으면 해당 채널에 유저 퇴장시 떠나보내는말이 뜨며, 끄기를 적으면 비활성화 됩니다!\n`%s접두사 [설정할 접두사]` - 봇의 접두사를 변경합니다! 한자리만 가능합니다!" % (prefix, prefix, prefix, prefix), inline=False)
                        embed.add_field(name="봇 관리자 명령어!", value="`rutap admin shutdown`\n`rutap admin game [Name]`\n`rutap admin debug help`\n`rutap admin (un)ban [ID]`\n`rutap admin notice -s all [...]`\n`rutap admin notice -s add [...]`\n`rutap admin notice -s channel [id]`", inline=False)
                        embed.add_field(name="문의", value="공식 지원서버 : https://invite.gg/rutapbot\n디스코드 : HwaHyang - Official#4037\n공식 트위터 : https://twitter.com/rutapofficial", inline=False)
                        embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                        log_actvity("I sent cmd list to %s." % (message.author.id))
                    elif message.author.server_permissions.administrator:
                        embed.add_field(name="서버 관리자 명령어!", value="`%sCC 추가 [원하는 명령어]` - 커스텀 커맨드(이하 CC)를 만들 수 있습니다. 서버당 5개 제한이 있습니다.\n`%s환영말 [할말 또는 끄기]` - 할말을 적으면 해당 채널에 유저 입장시 환영말이 뜨며, 끄기를 적으면 비활성화 됩니다!\n`%s나가는말 [할말 또는 끄기]` - 할말을 적으면 해당 채널에 유저 퇴장시 떠나보내는말이 뜨며, 끄기를 적으면 비활성화 됩니다!\n`%s접두사 [설정할 접두사]` - 봇의 접두사를 변경합니다! 한자리만 가능합니다!" % (prefix, prefix, prefix, prefix), inline=False)
                        embed.add_field(name="문의", value="공식 지원서버 : https://invite.gg/rutapbot\n디스코드 : HwaHyang - Official#4037\n공식 트위터 : https://twitter.com/rutapofficial", inline=False)
                        embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                        log_actvity("I sent cmd list to %s." % (message.author.id))
                    else:
                        embed.add_field(name="문의", value="공식 지원서버 : https://invite.gg/rutapbot\n디스코드 : HwaHyang - Official#4037\n공식 트위터 : https://twitter.com/rutapofficial", inline=False)
                        embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                        log_actvity("I sent cmd list to %s." % (message.author.id))

                if message.content == prefix + "도움말 전체":
                    embed = discord.Embed(title="루탑봇 전체 명령어!", description=None, color=0xb2ebf4)
                    embed.add_field(name="봇 관련 명령어!", value="`%s도움말` - 봇의 명령어를 출력합니다. `%s도움말 전체` 를 입력하여 모든 명령어를 볼 수 있습니다.\n`%s정보` - 봇의 정보를 출력합니다!" % (prefix, prefix, prefix), inline=False)
                    embed.add_field(name="봇 서버 관련 명령어!", value="`%s핑` - 현재 봇 서버의 응답속도를 확인합니다.\n`%s시간` - 현재 시간을 서버에서 가져옵니다." % (prefix, prefix), inline=False)
                    embed.add_field(name="정보 관련 명령어!", value="`%s서버정보` - 서버의 정보를 불러옵니다.\n|     아직은 노출할 수 있는 정보가 별로 없지만, 추후 지속적인 업데이트를 통하여 노출되는 정보를 추가할 예정입니다." % (prefix), inline=False)
                    embed.add_field(name="편의 관련 명령어!", value="`%s잠수 [사유]` - 잠수모드에 진입합니다. 타인이 자신을 언급하면 잠수중이라는 알림을 보냅니다.\n`%s이미지 [검색어]` - 구글에서 랜덤으로 사진 한장을 가져옵니다.\n`%s지우기 [숫자]` - 특정한 갯수의 메시지를 지울 수 있습니다!\n`%s냥이` - 랜덤으로 냥이 짤을 불러옵니다." % (prefix, prefix, prefix, prefix), inline=False)
                    embed.add_field(name="경고 관련 명령어!", value="`%s경고 확인` - 당신이 받은 경고 횟수를 확인합니다. 명령어 뒤에 멘션을 하여 특정 유저의 경고 상태를 볼 수 있습니다.\n`%s경고 부여 [멘션]`  - 경고를 부여합니다. 관리자 권한을 보유하고 있어야 가능합니다.\n`%s경고 제거 [멘션]`  - 경고를 제거합니다. 관리자 권한을 보유하고 있어야 가능합니다.\n`%s경고 초기화 [멘션]`  - 경고를 초기화합니다. 관리자 권한을 보유하고 있어야 가능합니다." % (prefix, prefix, prefix, prefix), inline=False)
                    embed.add_field(name="서버 관리자 명령어!", value="`%sCC 추가 [원하는 명령어]` - 커스텀 커맨드(이하 CC)를 만들 수 있습니다. 서버당 5개 제한이 있습니다.\n`%s환영말 [할말 또는 끄기]` - 할말을 적으면 해당 채널에 유저 입장시 환영말이 뜨며, 끄기를 적으면 비활성화 됩니다!\n`%s나가는말 [할말 또는 끄기]` - 할말을 적으면 해당 채널에 유저 퇴장시 떠나보내는말이 뜨며, 끄기를 적으면 비활성화 됩니다!\n`%s접두사 [설정할 접두사]` - 봇의 접두사를 변경합니다! 한자리만 가능합니다!" % (prefix, prefix, prefix, prefix), inline=False)
                    embed.add_field(name="봇 관리자 명령어!", value="`rutap admin shutdown`\n`rutap admin game [Name]`\n`rutap admin debug help`\n`rutap admin (un)ban [ID]`\n`rutap admin notice -s all [...]`\n`rutap admin notice -s add [...]`\n`rutap admin notice -s channel [id]`", inline=False)
                    embed.add_field(name="문의", value="공식 지원서버 : https://invite.gg/rutapbot\n디스코드 : HwaHyang - Official#4037\n공식 트위터 : https://twitter.com/rutapofficial", inline=False)
                    embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                    await app.send_message(message.channel, embed=embed) 
                    log_actvity("I sent all cmd list to %s." % (message.author.id))

                if message.content == prefix + "정보":
                    embed = discord.Embed(title="루탑봇 정보!", description=None, color=0xb2ebf4)
                    embed.add_field(name="[루탑봇 소개]", value="https://rutapofficial.xyz/redirect/about/rutap", inline=False)
                    embed.add_field(name="[루탑봇 개발자]", value="화향", inline=False)
                    embed.add_field(name="[Special Thanks To]", value="The_Adminator", inline=False)
                    embed.add_field(name="[오픈소스 라이선스]", value="This bot use nekos.life API. : https://discord.services/api/\n\nhttps://github.com/kijk2869/Discord-Python-Notice-Korean\n(GNU General Public License v3.0)", inline=False)
                    embed.add_field(name="[Team. 화공 공식 링크]", value="공식 홈페이지 : https://rutapofficial.xyz/\n공식 트위터 : https://twitter.com/rutapofficial\n공식 디스코드 : https://invite.gg/rutapbot", inline=False)
                    embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                    await app.send_message(message.channel, embed=embed)
                    log_actvity("I sent Bot info to %s." % (message.author.id))

                if prefix + "서버정보" == message.content:
                    embed = discord.Embed(title="\"%s\" 서버정보!" % (message.server.name), description=None, color=0xb2ebf4)
                    embed.add_field(name="서버 소유자", value="<@%s>" % message.server.owner.id, inline=False)
                    embed.add_field(name="서버 생성일", value="%s (UTC)" % (message.server.created_at), inline=False)
                    embed.add_field(name="서버 보안등급", value=message.server.verification_level, inline=False)
                    embed.add_field(name="서버 위치", value=message.server.region, inline=False)
                    embed.add_field(name="서버 잠수채널", value="%s (%s분 이상 잠수이면 이동됨)" % (message.server.afk_channel, message.server.afk_timeout/60), inline=False)
                    embed.add_field(name="커스텀커맨드 추가 가능 횟수", value="%s회" % (open("Server_%s/%s_Server_CC_Limit.rtl" % (message.server.id, message.server.id), 'r').read()), inline=False)
                    embed.set_thumbnail(url=message.server.icon_url)
                    embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                    await app.send_message(message.channel, embed=embed)
                    log_actvity("I sent Server info to %s." % (message.author.id))

                if message.content.startswith(prefix + '경고 확인'):
                    mention_id = message.author.id
                    if message.content[7:].startswith('<') and message.content.endswith('>'):
                        mention_id = re.findall(r'\d+', message.content)
                        mention_id = mention_id[0]
                        mention_id = str(mention_id)
                        if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
                            f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'r')
                            warn_num = f.read()
                            f.close()
                            embed = discord.Embed(title="경고 스탯!", description=None, color=0xb2ebf4)
                            embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=True)
                            embed.add_field(name="총 경고", value="%s회" % (warn_num), inline=True)
                            embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                            log_actvity("%s has confirmed %s's warning. (warn_num : %s)" % (message.author.id, mention_id, warn_num))
                        else:
                            embed = discord.Embed(title="경고 스탯!", description=None, color=0xb2ebf4)
                            embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=True)
                            embed.add_field(name="총 경고", value="0회", inline=True)
                            embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                            log_actvity("%s has confirmed %s's warning. (warn_num : 0)" % (message.author.id, mention_id))
                    else:
                        if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
                            f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'r')
                            warn_num = f.read()
                            f.close()
                            embed = discord.Embed(title="경고 스탯!", description=None, color=0xb2ebf4)
                            embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=True)
                            embed.add_field(name="총 경고", value="%s회" % (warn_num), inline=True)
                            embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                            log_actvity("%s has confirmed his warning. (warn_num : %s)" % (message.author.id, warn_num))
                        else:
                            embed = discord.Embed(title="경고 스탯!", description=None, color=0xb2ebf4)
                            embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=True)
                            embed.add_field(name="총 경고", value="0회", inline=True)
                            embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                            log_actvity("%s has confirmed his warning. (warn_num : 0)" % (message.author.id))

                if message.content.startswith(prefix + '경고 부여'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        if message.content[7:].startswith('<') and message.content.endswith('>'):
                            mention_id = re.findall(r'\d+', message.content)
                            mention_id = mention_id[0]
                            mention_id = str(mention_id)
                            if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
                                f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'r')
                                past_warn = f.read()
                                f.close()
                                now_warn = int(past_warn) + int(1)
                                now_warn = str(now_warn)
                                f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'w')
                                f.write(now_warn)
                                f.close()
                                embed = discord.Embed(title="경고가 발생했습니다!", description=None, color=0xb2ebf4)
                                embed.add_field(name="관리자", value="<@%s>" % (message.author.id), inline=True)
                                embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=True)
                                embed.add_field(name="총 경고", value="%s회" % (now_warn), inline=True)
                                embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                                await app.send_message(message.channel, embed=embed)
                                log_actvity("%s has gived %s's warn (now : %s)" % (message.author.id, mention_id, now_warn))
                            else:
                                f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'w')
                                f.write(str(1))
                                f.close()
                                embed = discord.Embed(title="경고가 발생했습니다!", description=None, color=0xb2ebf4)
                                embed.add_field(name="관리자", value="<@%s>" % (message.author.id), inline=True)
                                embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=True)
                                embed.add_field(name="총 경고", value="1회", inline=True)
                                embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                                await app.send_message(message.channel, embed=embed)
                                log_actvity("%s has gived %s's warn (now : 1)" % (message.author.id, mention_id))
                        else:
                            await app.send_message(message.channel, "<@%s>, 유저를 언급해야 합니다!" % (message.author.id))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자가 아닙니다!" % (message.author.id))

                if message.content.startswith(prefix + '경고 제거'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        if message.content[7:].startswith('<') and message.content.endswith('>'):
                            mention_id = re.findall(r'\d+', message.content)
                            mention_id = mention_id[0]
                            mention_id = str(mention_id)
                            if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
                                f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'r')
                                past_warn = f.read()
                                f.close()
                                now_warn = int(past_warn) - int(1)
                                now_warn = str(now_warn)
                                f = open("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id), 'w')
                                f.write(now_warn)
                                f.close()
                                embed = discord.Embed(title="경고 철회가 발생했습니다!", description=None, color=0xb2ebf4)
                                embed.add_field(name="관리자", value="<@%s>" % (message.author.id), inline=True)
                                embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=True)
                                embed.add_field(name="총 경고", value="%s회" % (now_warn), inline=True)
                                embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                                await app.send_message(message.channel, embed=embed)
                                log_actvity("%s has removed %s's warn (now : %s)" % (message.author.id, mention_id, now_warn))
                            else:
                                await app.send_message(message.channel, "<@%s>, 대상 유저는 경고를 보유하고 있지 않습니다!" % (message.author.id))
                        else:
                            await app.send_message(message.channel, "<@%s>, 유저를 언급해야 합니다!" % (message.author.id))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자가 아닙니다!" % (message.author.id))

                if message.content.startswith(prefix + '경고 초기화'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        if message.content[8:].startswith('<') and message.content.endswith('>'):
                            mention_id = re.findall(r'\d+', message.content)
                            mention_id = mention_id[0]
                            mention_id = str(mention_id)
                            if os.path.isfile("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id)):
                                os.remove("Server_%s/warn_user_%s.txt" % (message.server.id, mention_id))
                                embed = discord.Embed(title="경고 초기화가 발생했습니다!", description=None, color=0xb2ebf4)
                                embed.add_field(name="관리자", value="<@%s>" % (message.author.id), inline=True)
                                embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=True)
                                embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                                await app.send_message(message.channel, embed=embed)
                                log_actvity("%s has reset %s's warn" % (message.author.id, mention_id))
                            else:
                                await app.send_message(message.channel, "<@%s>, 대상 유저는 경고를 보유하고 있지 않습니다!" % (message.author.id))
                        else:
                            await app.send_message(message.channel, "<@%s>, 유저를 언급해야 합니다!" % (message.author.id))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자가 아닙니다!" % (message.author.id))

                if message.content == prefix + "냥이":
                    waitmsg = await app.send_message(message.channel, "<@%s>,\nnekos.life API부터로의 응답을 기다리고 있습니다. 최장 10초가 소요됩니다." % (message.author.id))
                    #nekos.life API 사용 구문 시점
                    r = requests.get("https://nekos.life/api/v2/img/neko")
                    r = r.text
                    data = json.loads(r)
                    file = data["url"]
                    #nekos.life API 사용 구문 종점
                    embed=discord.Embed(title=None, description=None, color=0xb2ebf4)
                    embed.set_image(url=file)
                    embed.set_footer(text = "Powered By. nekos.life | Ver. %s | %s" % (Setting.version, Copyright))
                    await app.delete_message(waitmsg)
                    await app.send_message(message.channel, "<@%s>," % (message.author.id), embed=embed)
                    log_actvity("I sent %s to %s." % (file, message.author.id))

                if message.content.startswith(prefix + 'CC 추가') or message.content.startswith(prefix + 'cc 추가'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        if os.path.isfile("Server_%s/%s_Server_%s_Query.rtl" % (message.server.id, message.server.id, message.author.id)):
                            await app.send_message(message.channel, "<@%s>, 현재 추가 요청하신 커스텀커맨드가 있습니다!\n잠시 후 다시 시도하여 주세요!" % (message.author.id))
                        else:
                            limit = open("Server_%s/%s_Server_CC_Limit.rtl" % (message.server.id, message.server.id), 'r').read()
                            if float(limit) - 1 < 1:
                                await app.send_message(message.channel, "<@%s>, 커스텀커맨드 제한(`%s회`)을 초과했습니다!" % (message.author.id, limit))
                            else:
                                if message.content[7:] == "":
                                    await app.send_message(message.channel, "<@%s>, 누락된 항목이 있습니다. 다시 한번 확인 해 주세요!" % (message.author.id))
                                else:
                                    if os.path.isfile("Server_%s/%s_Server_CC_%s" % (message.server.id, message.server.id, message.content[11:])):
                                        await app.send_message(message.channel, "<@%s>, 해당 커스텀커맨드(`%s`)가 이미 존재합니다!" % (message.author.id, message.content[11:]))
                                    else:
                                        cc_q = message.content[7:]
                                        open("Server_%s/%s_Server_%s_Query.rtl" % (message.server.id, message.server.id, message.author.id), 'w').write(cc_q)
                                        embed = discord.Embed(title="이제 한단계 남았습니다!", description="`%s%s` 명령어를 추가하시려면 `%sCC 등록 [CC 입력시 봇이 할 말]` 을 30초 내로 적어주세요!\n**__이미지는 링크(주소)로 보내셔야 합니다!__**" % (prefix, cc_q, prefix), color=0xb2ebf4)
                                        embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                                        await app.send_message(message.channel, "<@%s>," % (message.author.id), embed=embed)
                                        await asyncio.sleep(30)
                                        if os.path.isfile("Server_%s/%s_Server_%s_Query.rtl" % (message.server.id, message.server.id, message.author.id)):
                                            os.remove("Server_%s/%s_Server_%s_Query.rtl" % (message.server.id, message.server.id, message.author.id))
                                            await app.send_message(message.channel, "<@%s>, 커스텀커맨드(`%s%s`) 추가 요청이 시간초과로 취소되었습니다. 다시 시도하여 주세요!" % (message.author.id, prefix, cc_q))
                                        else:
                                            return None
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

                if message.content.startswith(prefix + 'CC 등록') or message.content.startswith(prefix + 'cc 등록'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        if os.path.isfile("Server_%s/%s_Server_%s_Query.rtl" % (message.server.id, message.server.id, message.author.id)):
                            cc = open("Server_%s/%s_Server_%s_Query.rtl" % (message.server.id, message.server.id, message.author.id), 'r').read()
                            os.remove("Server_%s/%s_Server_%s_Query.rtl" % (message.server.id, message.server.id, message.author.id))
                            q = message.content[7:]
                            open("Server_%s/%s_Server_CC_%s.rts" % (message.server.id, message.server.id, cc), 'w').write(q)
                            limit = float(open("Server_%s/%s_Server_CC_Limit.rtl" % (message.server.id, message.server.id), 'r').read())
                            open("Server_%s/%s_Server_CC_Limit.rtl" % (message.server.id, message.server.id), 'w').write(str(limit - 1))
                            embed = discord.Embed(title="완료되었습니다!", description="요청하신 커스텀커맨드 `%s%s`가 등록되었습니다!\n`%s%s`을(를) 입력 해 보세요!\n\n오류를 방지하기 위해, 다음 커스텀 커맨드 신청은 30초 뒤에 해주세요!" % (prefix, cc, prefix, cc), color=0xb2ebf4)
                            embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, "<@%s>," % (message.author.id), embed=embed)
                        else:
                            await app.send_message(message.channel, "<@%s>, 신청하신 커스텀커맨드가 없습니다! `%sCC 추가`로 커스텀커맨드 추가를 신청하세요!" % (message.author.id, prefix))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

                if message.content.startswith(prefix + 'CC 제거') or message.content.startswith(prefix + 'cc 제거'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        if os.path.isfile("Server_%s/%s_Server_%s_Query.rtl" % (message.server.id, message.server.id, message.author.id)):
                            await app.send_message(message.channel, "<@%s>, 현재 추가 요청하신 커스텀커맨드가 있습니다!\n잠시 후 다시 시도하여 주세요!" % (message.author.id))
                        else:
                            if message.content[7:] == "":
                                await app.send_message(message.channel, "<@%s>, 누락된 항목이 있습니다. 다시 한번 확인 해 주세요!" % (message.author.id))
                            else:
                                if os.path.isfile("Server_%s/%s_Server_CC_%s.rts" % (message.server.id, message.server.id, message.content[7:])):
                                    limit = float(open("Server_%s/%s_Server_CC_Limit.rtl" % (message.server.id, message.server.id), 'r').read())
                                    open("Server_%s/%s_Server_CC_Limit.rtl" % (message.server.id, message.server.id), 'w').write(str(limit + 1.0))
                                    os.remove("Server_%s/%s_Server_CC_%s.rts" % (message.server.id, message.server.id, message.content[7:]))
                                    embed = discord.Embed(title="완료되었습니다!", description="요청하신 커스텀커맨드 `%s%s`가 삭제되었습니다!" % (prefix, message.content[7:]), color=0xb2ebf4)
                                    embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                                    await app.send_message(message.channel, "<@%s>," % (message.author.id), embed=embed)
                                else:
                                    await app.send_message(message.channel, "<@%s>, 해당 커스텀커맨드(`%s`)가 존재하지 않습니다!" % (message.author.id, message.content[7:]))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

                if message.content.startswith(prefix + '환영말'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        if message.content[5:].startswith('끄기'):
                            if os.path.isfile("Server_%s/%sServer_welcome_say_channel.rts" % (message.server.id, message.server.id)):
                                os.remove("Server_%s/%sServer_welcome_say_channel.rts" % (message.server.id, message.server.id))
                                os.remove("Server_%s/%sServer_welcome_msg.rts" % (message.server.id, message.server.id))
                                embed = discord.Embed(title="완료!", description="앞으로 유저 입장시 환영말이 뜨지 않습니다!", color=0xb2ebf4)
                                embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                                await app.send_message(message.channel, embed=embed)
                                log_actvity("%s has off the welcome message." % (message.author.id))
                            else:
                                await app.send_message(message.channel, "<@%s>, 설정한 환영말이 없습니다!" % (message.author.id))
                        else: 
                            welcome_msg = message.content[5:]
                            open("Server_%s/%sServer_welcome_say_channel.rts" % (message.server.id, message.server.id), 'w').write(message.channel.id)
                            open("Server_%s/%sServer_welcome_msg.rts" % (message.server.id, message.server.id), 'w').write(welcome_msg)
                            embed = discord.Embed(title="완료!", description="앞으로 이 채널에 환영말이 전송됩니다!", color=0xb2ebf4)
                            embed.add_field(name="설정한 환영말", value="`(유저언급), %s`" % (welcome_msg), inline=False)
                            embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                            log_actvity("%s has set the welcome message. (msg : (Mention), %s)" % (message.author.id, welcome_msg))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))
    
                if message.content.startswith(prefix + '나가는말'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        if message.content[6:].startswith('끄기'):
                            if os.path.isfile("Server_%s/%sServer_bye_say_channel.rts" % (message.server.id, message.server.id)):
                                os.remove("Server_%s/%sServer_bye_say_channel.rts" % (message.server.id, message.server.id))
                                os.remove("Server_%s/%sServer_bye_msg.rts" % (message.server.id, message.server.id))
                                embed = discord.Embed(title="완료!", description="앞으로 유저 퇴장시 나가는말이 뜨지 않습니다!", color=0xb2ebf4)
                                embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                                await app.send_message(message.channel, embed=embed)
                                log_actvity("%s has off the bye message." % (message.author.id))
                            else:
                                await app.send_message(message.channel, "<@%s>, 설정한 나가는말이 없습니다!" % (message.author.id))
                        else: 
                            bye_msg = message.content[6:]
                            open("Server_%s/%sServer_bye_say_channel.rts" % (message.server.id, message.server.id), 'w').write(message.channel.id)
                            open("Server_%s/%sServer_bye_msg.rts" % (message.server.id, message.server.id), 'w').write(bye_msg)
                            embed = discord.Embed(title="완료!", description="앞으로 이 채널에 나가는말이 기록됩니다!", color=0xb2ebf4)
                            embed.add_field(name="설정한 나가는말", value="`(유저언급), %s`" % (bye_msg), inline=False)
                            embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                            log_actvity("%s has set the bye message. (msg : (Mention), %s)" % (message.author.id, bye_msg))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

                if message.content.startswith(prefix + '접두사'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        prefix_change = message.content[5:6]
                        if prefix_change == "`":
                            await app.send_message(message.channel, "<@%s>, 해당 접두사는 오류가 발생 할 수 있어 사용 할 수 없습니다!" % (message.author.id))
                        else:
                            open("Server_%s/%s_Server_prefix.rts" % (message.server.id, message.server.id), 'w').write(prefix_change)
                            embed = discord.Embed(title="해당 서버의 접두사가 변경되었습니다!", description="접두사가 `%s`에서 `%s`으로 변경되었습니다!" % (prefix, prefix_change), color=0xb2ebf4)
                            embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                            log_actvity("%s has changed prefix to %s in %s (was : %s)" % (message.author.id, prefix_change, message.server.id, prefix))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

                if prefix + "핑" == message.content:
                    if os.path.isfile('no_ping.txt'):
                        await app.send_message(message.channel, "<@" + message.author.id + ">,  서버의 안전을 위하여 상태를 한번에 여러명이 조회 할 수 없습니다!\n잠시 후 다시 시도 해 주세요!")
                    else:
                        f = open("no_ping.txt", 'w').close()

                        msgarrived = float(str(time.time())[:-3])
                        msgtime = timeform(message.timestamp)
                        msgdelay = msgarrived - msgtime - 32400
                        ping = int(msgdelay * 1000)

                        embed = discord.Embed(title="루탑봇 상태!", description=None, color=0xb2ebf4)
                        if 0 < ping < 400:
                            embed.add_field(name="서버 핑", value="`%sms`(:large_blue_circle: 핑이 정상입니다.)" % (str(ping)), inline=False)
                            embed.add_field(name="봇 업타임", value="https://status.hwahyang.xyz/", inline=False)
                            embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                            await app.send_message(message.channel, "<@%s>, " % (message.author.id), embed=embed)
                            os.remove("no_ping.txt")
                            log_actvity("I sent ping to %s. (ping : %sms)" % (message.author.id, str(ping)))
                        elif ping > 399:
                            embed.add_field(name="서버 핑", value="`%sms`(:red_circle: 핑이 비정상입니다.)" % (str(ping)), inline=False)
                            embed.add_field(name="봇 업타임", value="https://status.hwahyang.xyz/", inline=False)
                            embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                            await app.send_message(message.channel, "<@%s>, " % (message.author.id), embed=embed)
                            os.remove("no_ping.txt")
                            log_actvity("I sent ping to %s. (ping : %sms)" % (message.author.id, str(ping)))
                        else:
                            embed.add_field(name="서버 핑", value="`%sms`(:question: 결과 도출 도중 문제가 발생했습니다.)" % (str(ping)), inline=False)
                            embed.add_field(name="봇 업타임", value="https://status.hwahyang.xyz/", inline=False)
                            embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                            await app.send_message(message.channel, "<@%s>, " % (message.author.id), embed=embed)
                            os.remove("no_ping.txt")
                            log_actvity("I sent ping to %s. (ping : %sms)" % (message.author.id, str(ping)))

                if message.content.startswith(prefix + '잠수'):

                    if os.path.isfile("afk" + message.author.id + "txt"):
                        return None
                    else:

                        imafk = message.content[4:]

                        open("afk/afk_year%s.rtl" % (message.author.id), 'w').write(str(now.year))
                        open("afk/afk_month%s.rtl" % (message.author.id), 'w').write(str(now.month))
                        open("afk/afk_day%s.rtl" % (message.author.id), 'w').write(str(now.day))
                        open("afk/afk_hour%s.rtl" % (message.author.id), 'w').write(str(now.hour))
                        open("afk/afk_min%s.rtl" % (message.author.id), 'w').write(str(now.minute))
                        open("afk/afk_because%s.rtl" % (message.author.id), 'w').write(imafk)

                        embed = discord.Embed(title="잠수시작!", description=None, color=0xb2ebf4)
                        embed.add_field(name="대상 유저", value="<@%s>" % (message.author.id), inline=False)
                        embed.add_field(name="사유", value=imafk, inline=False)
                        embed.add_field(name="잠수 시작 시간", value="%s/%s/%s | %s:%s" % (str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute)), inline=True)
                        embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                        log_actvity("%s started AFK." % (message.author.id))

                if "<@" in message.content:
                    mention_id = re.findall(r'\d+', message.content)
                    mention_id = mention_id[0]
                    mention_id = str(mention_id)
                    if os.path.isfile("afk/afk_because%s.rtl" % (mention_id)):

                        year = open("afk/afk_year%s.rtl" % (mention_id), 'r').read()
                        month = open("afk/afk_month%s.rtl" % (mention_id), 'r').read()
                        day = open("afk/afk_day%s.rtl" % (mention_id), 'r').read()
                        hour = open("afk/afk_hour%s.rtl" % (mention_id), 'r').read()
                        minute = open("afk/afk_min%s.rtl" % (mention_id), 'r').read()
                        imafk = open("afk/afk_because%s.rtl" % (mention_id), 'r').read()

                        embed = discord.Embed(title="잠수 상태!", description=None, color=0xb2ebf4)
                        embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=False)
                        embed.add_field(name="사유", value=imafk, inline=False)
                        embed.add_field(name="잠수 시작 시간", value="%s/%s/%s | %s:%s" % (str(year), str(month), str(day), str(hour), str(minute)), inline=True)
                        embed.add_field(name="현재 시간", value="%s/%s/%s | %s:%s" % (str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute)), inline=True)
                        embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, "<@%s>, 해당 유저는 현재 잠수 중 입니다!" % (message.author.id) ,embed=embed)
                        log_actvity("%s is AFK now. so I sent a notification to %s" % (mention_id, message.author.id))
                    else:
                        return None

                if message.content.startswith(prefix + '이미지'):
                    waitmsg = await app.send_message(message.channel, "<@%s>,\nGoogle.co.kr 부터로의 응답을 기다리고 있습니다. 최장 10초가 소요됩니다." % (message.author.id))

                    q = message.content[5:]
                    q = q.encode("raw_unicode_escape")
                    q = str(q)

                    data = requests.get("https://www.google.co.kr/search?q=" + q + "&source=lnms&tbm=isch&sa=X")
                    soup = bs4(data.text, "html.parser")
                    imgs = soup.find_all("img")

                    file = random.choice(imgs[1:])['src']

                    await app.delete_message(waitmsg)
                    embed = discord.Embed(title="\"%s\"에 대한 검색 결과" % (message.content[5:]), description=None, color=0xb2ebf4)
                    embed.set_image(url=file)
                    embed.set_footer(text = "Powered By. google.co.kr | Ver. %s | %s" % (Setting.version, Copyright))
                    await app.send_message(message.channel, "<@%s>" % (message.author.id), embed=embed)
                    log_actvity("I sent %s to %s. (Search query : %s)" % (file, message.author.id, message.content[5:]))

                if message.content.startswith(prefix + '시간'):
                    if now.hour > 12:
                        embed = discord.Embed(title="현재 서버 시간은 %s년 %s월 %s일 오후 %s시 %s분 %s초 입니다!" % (now.year, now.month, now.day, now.hour - 12, now.minute, now.second), description=None, color=0xb2ebf4)
                        embed.set_footer(text = "Seoul. (GMT +09:00) | Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                        log_actvity("I sent Current time to %s." % (message.author.id))
                    else:
                        embed = discord.Embed(title="현재 서버 시간은 %s년 %s월 %s일 오전 %s시 %s분 %s초 입니다!" % (now.year, now.month, now.day, now.hour, now.minute, now.second), description=None, color=0xb2ebf4)
                        embed.set_footer(text = "Seoul. (GMT +09:00) | Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                        log_actvity("I sent Current time to %s." % (message.author.id))


                if message.content.startswith(prefix + '지우기'):
                    if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                        if int(0) < int(message.content[5:]):
                            await app.send_message(message.channel, embed=discord.Embed(color=0xb2ebf4, title="모듈 초기화중..."))
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
                                returnmsg = await app.send_message(message.channel, embed=discord.Embed(color=0xb2ebf4, title="%s개의 메세지를 삭제하였으며, 0개의 메시지를 삭제하지 못하였습니다." % (cleared), description=""))
                                await asyncio.sleep(3)
                                await app.delete_message(returnmsg)
                                log_actvity("%s messages have been deleted by %s. (failed : 0)" % (cleared, message.author.id))
                            else:
                                returnmsg = await app.send_message(message.channel, embed=discord.Embed(color=0xb2ebf4, title="%s개의 메세지를 삭제하였으며, %s개의 메시지를 삭제하지 못하였습니다." % (cleared, failed), description="(추정 원인 : 메시지 관리 권한이 없거나, 너무 오래된 메시지 입니다)"))
                                await asyncio.sleep(5)
                                await app.delete_message(returnmsg)
                                log_actvity("%s messages have been deleted by %s. (failed : %s)" % (cleared, message.author.id, failed))
                        else:
                            await app.send_message(message.channel, "<@%s>, 지울 만큼의 메세지 수를 제대로 적어주세요!" % (message.author.id))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

            else:
                if os.path.isfile("Server_%s/%s_Server_first.rtl" % (message.server.id, message.server.id)):
                    if message.content == "루탑봇 활성화":
                        if message.author.server_permissions.administrator or message.author.id == Setting.owner_id:
                            os.remove("Server_%s/%s_Server_first.rtl" % (message.server.id, message.server.id))
                            open("Server_%s/%s_Server_prefix.rts" % (message.server.id, message.server.id), 'w').write(Setting.prefix)
                            open("Server_%s/%s_Server_CC_Limit.rtl" % (message.server.id, message.server.id), 'w').write("3")
                            embed = discord.Embed(title="루탑봇이 해당 서버에 활성화 되었습니다!", description="기본 접두사는 ``%s`` 이며, ``%s도움말``로 기본 명령어를 확인하세요!" % (Setting.prefix, Setting.prefix), color=0xb2ebf4)
                            embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                            log_actvity("Logging Started In %s (by %s)" % (message.server.id, message.author.id))
                        else:
                            await app.send_file(message.channel, "<@%s>, 서버 관리자만이 봇을 활성화 시킬 수 있습니다!")
                    else:
                        return None
                else:
                    embed = discord.Embed(title="환영합니다!", description=None, color=0xb2ebf4)
                    embed.add_field(name="루탑봇을 초대 해 주셔서 감사합니다!", value="루탑봇을 활성화 하시려면 서버 관리자가 ``루탑봇 활성화``를 입력 해 주세요!", inline=False)
                    embed.add_field(name="주의하세요!", value="**루탑봇 활성화를 하면 서버 관리자가 모든 유저를 대표하여 이용약관과 개인정보 취급방침에 동의하는 것으로 간주됩니다.\n이를 원하지 않으시면 루탑봇을 추방하여 주세요.**", inline=False)
                    embed.add_field(name="링크", value="개인정보 처리방침 : https://rutapofficial.xyz/post/18/\n이용약관 : https://rutapofficial.xyz/post/21/")
                    embed.add_field(name="문의", value="공식 홈페이지 : https://ruapofficial.xyz\n공식 지원서버 : https://invite.gg/rutapbot\n디스코드 : HwaHyang - Official#4037\n공식 트위터 : https://twitter.com/rutapofficial")
                    embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                    await app.send_message(message.channel, embed=embed)
                    try:
                        os.makedirs("Server_%s" %(message.server.id))
                    except:
                        a = 0
                    open("Server_%s/%s_Server_first.rtl" % (message.server.id, message.server.id), 'w').close()
        except discord.HTTPException as e:
                embed = discord.Embed(title="죄송합니다. 예기치 못한 애러가 발생했습니다.", description="봇이 메시지 관련한 충분한 권한을 가지고 있는지 다시 한 번 확인 해 주시기 바랍니다.\nOfficial Support Server : https://invite.gg/rutapbot", color=0xff0000)
                embed.set_footer(text = e)
                await app.send_message(message.author, embed=embed)
                log_actvity("Discord HTTPException has occured in %s(%s) | %s(%s) : %s" % (message.server.id, message.server.name, message.channel.id, message.channel, e))
    except Exception as e:
        try:
            embed = discord.Embed(title="죄송합니다. 원인을 알 수 없는 애러가 발생했습니다.", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주시기 바랍니다.\nOfficial Support Server : https://invite.gg/rutapbot", color=0xff0000)
            embed.set_footer(text = e)
            await app.send_message(message.channel, embed=embed)
            log_actvity("Err has occured in %s : %s" % (message.content, e))
        except discord.HTTPException as e:
            return None # 위에서 HTTPException 잡아서 출력하니까 여기서 HTTPException 애러나는데 왜나는지 모르겠음

app.run(Setting.token)
