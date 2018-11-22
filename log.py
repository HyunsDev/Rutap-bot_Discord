# -*- coding: utf-8 -*- 

######################################################
#              Rutap Bot Logging Module              #
# Copyright 2018 Team. Hwagong. All Rights Reserved. #
# 모든 저작권은 2018 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
######################################################

import asyncio
import discord  # 디스코드 모듈
import sys
import os
import datetime

import general_settings  # 설정관리 모듈

Setting = general_settings.Settings()  # 설정 불러오기

app = discord.Client()  # 챗봇 지정

bot_deleting = False

@app.event
async def on_ready():
    now = datetime.datetime.now()

    f = open(Setting.log_file, 'r', encoding='UTF8')
    past_log = f.read()
    f.close()

    now_log = past_log + "\n\n" + str(now.year) + " / " + str(now.month) + " / " + str(now.day) + " | " + str(now.hour) + " : " + str(now.minute) + " | Logging Started.\n"

    f = open(Setting.log_file, 'w', encoding='UTF8')
    f.write(now_log)
    f.close()

    print(app.user.name, "(%s)" % app.user.id)

# --- 이벤트영역 ---

# 메세지가 삭제되었을 때
@app.event
async def on_message_delete(message):
    global bot_deleting
    now = datetime.datetime.now()
    try:
        if os.path.isfile("non-del.txt"):
            os.remove("non-del.txt")
            f = open(Setting.log_file, 'r', encoding='UTF8')
            past_log = f.read()
            f.close()

            now_log = past_log + "\n" + str(now.year) + " / " + str(now.month) + " / " + str(now.day) + " | " + str(now.hour) + " : " + str(now.minute) + " | Server : %s(%s) | Channel: %s(%s) | %s%s(%s) 님이 작성한 메시지가 삭제되었으며, 시스템에서 삭제한 메시지 입니다." % (
                message.server, message.server.id,
                message.channel, message.channel.id,
                message.author.name, "#"+message.author.discriminator,
                message.author.id
            )

            f = open(Setting.log_file, 'w', encoding='UTF8')
            f.write(now_log)
            f.close()
        else:
            f = open(Setting.log_file, 'r', encoding='UTF8')
            past_log = f.read()
            f.close()

            now_log = past_log + "\n" + str(now.year) + " / " + str(now.month) + " / " + str(now.day) + " | " + str(now.hour) + " : " + str(now.minute) + " | Server : %s(%s) | Channel: %s(%s) | %s%s(%s) 님이 작성한 메시지가 삭제되었습니다." % (
                message.server, message.server.id,
                message.channel, message.channel.id,
                message.author.name, "#"+message.author.discriminator,
                message.author.id
            )

            f = open(Setting.log_file, 'w', encoding='UTF8')
            f.write(now_log)
            f.close()
    except Exception as er:
        f = open(Setting.log_file, 'r', encoding='UTF8')
        past_log = f.read()
        f.close()

        now_log = past_log + "\n" + str(now.year) + " / " + str(now.month) + " / " + str(now.day) + " | " + str(now.hour) + " : " + str(now.minute) + " | 삭제된 메시지 로그 작성 도중 애러가 발생하였습니다. : %s" % (
            er
        )

        f = open(Setting.log_file, 'w', encoding='UTF8')
        f.write(now_log)
        f.close()

# 메세지
@app.event
async def on_message(message):

    if message.author.id == "0": 
        return None
    else:
        now = datetime.datetime.now()
        try:
            if int(message.author.id) == 298822483060981760 or int(message.channel.id) == 479999656567504906 or int(message.channel.id) == 480273079885627395 or int(message.channel.id) == 480277251049652225:
                return None
            else:
                f = open(Setting.log_file, 'r', encoding='UTF8')
                past_log = f.read()
                f.close()

                now_log = past_log + "\n" + str(now.year) + " / " + str(now.month) + " / " + str(now.day) + " | " + str(now.hour) + " : " + str(now.minute) + " | Server : %s(%s) | Channel: %s(%s) | Author: %s%s(%s) | Message: %s" % (
                    message.server, message.server.id,
                    message.channel, message.channel.id,
                    message.author.name, "#"+message.author.discriminator,
                    message.author.id, message.content
                )

                f = open(Setting.log_file, 'w', encoding='UTF8')
                f.write(now_log)
                f.close()
        except Exception as er:
            f = open(Setting.log_file, 'r', encoding='UTF8')
            past_log = f.read()
            f.close()

            now_log = past_log + "\n" + str(now.year) + " / " + str(now.month) + " / " + str(now.day) + " | " + str(now.hour) + " : " + str(now.minute) + " | 메시지 로그 작성 도중 애러가 발생하였습니다. | %s" % (
                er
            )

            f = open(Setting.log_file, 'w', encoding='UTF8')
            f.write(now_log)
            f.close()

    #익명로그
    if Setting.prefix + "익명" == message.content.split(" ")[0]:
        if os.path.isfile("%sServer_say_logging_channel" % (
            message.server.id
        )):
            f = open("%sServer_say_logging_channel" % (
                message.server.id
            ), 'r')
            channel = f.read()
            f.close()
            embed = discord.Embed(title="", description="<@%s>님이 사용하신 익명 내용입니다.\n\n```%s```" % (
                message.author.id, message.content[4:]
            ), color=0x00ff00)
            embed.set_footer(text = "Server id : " + message.server.id + " | Ver. " + Setting.version + " | © 2018 Team. 화공")
            await app.send_message(app.get_channel(channel), embed=embed)
        else:
            return None

    #리붓하고 종료
    if Setting.prefix + "rutap admin shutdown" == message.content:
        try:
            if message.author.id =="440501082720960522":
                await app.send_message(message.channel, "<@" + message.author.id + ">, Shutdown the logging Module(log.py)!")
                exit()
            elif message.author.id == "357857022974230538":
                await app.send_message(message.channel, "<@" + message.author.id + ">, Shutdown the logging Module(log.py)!")
                exit()
            else:
                return None
        except Exception as er:
            print(er)

    if Setting.prefix + "rutap admin restart" == message.content:
        try:
            if message.author.id =="440501082720960522":
                await app.send_message(message.channel, "<@" + message.author.id + ">, Restart the logging Module(log.py)!")
                python = sys.executable
                os.execl(python, python, * sys.argv)
            elif message.author.id == "357857022974230538":
                await app.send_message(message.channel, "<@" + message.author.id + ">, Restart the logging Module(log.py)!")
                python = sys.executable
                os.execl(python, python, * sys.argv)
            else:
                return None
        except Exception as er:
            print(er)

# 봇 실행
app.run(Setting.token)
