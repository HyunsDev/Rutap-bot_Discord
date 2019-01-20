# -*- coding:utf-8 -*- 

###############################################################################
#                     Rutap Bot 2019 Hangul Clock Module                      #
# 해당 모듈은 한글시계에서 파생된 소프트웨어로서, GPLv3 라이선스의 적용을 받습니다. #
#                모듈 사용시 원작자분께 허락을 받으시길 바랍니다.                 #
#                    모듈에 대한 저작권은 화향이 소유합니다.                     #
###############################################################################

import random, datetime, os
import numpy as np
from PIL import Image
from activity_log import log_actvity

def alpha_composite(src, dst):
    src = np.asarray(src)
    dst = np.asarray(dst)
    out = np.empty(src.shape, dtype = 'float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    src_a = src[alpha]/255.0
    dst_a = dst[alpha]/255.0
    out[alpha] = src_a+dst_a*(1-src_a)
    old_setting = np.seterr(invalid = 'ignore')
    out[rgb] = (src[rgb]*src_a + dst[rgb]*dst_a*(1-src_a))/out[alpha]
    np.seterr(**old_setting)
    out[alpha] *= 255
    np.clip(out,0,255)
    out = out.astype('uint8')
    out = Image.fromarray(out, 'RGBA')
    return out

def hangul_clock():
    open('clock_rendering.rtl', 'w').close()

    now = datetime.datetime.now()
    filename = "%s_%s_%s_%s_%s_%s.png" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

    BG = Image.open("hangul_clock_base/BG_1000_1500.png")
    ment = Image.open("hangul_clock_base/ment/ment%s_1000_1500.png" % (random.randint(1, 3)))
    one = alpha_composite(ment, BG)

    hour_base = Image.open("hangul_clock_base/hour/hour_base_1000_1500.png")
    two = alpha_composite(hour_base, one)

    min_base = Image.open("hangul_clock_base/minute/minute_base_1000_1500.png")
    three = alpha_composite(min_base, two)

    hour = now.hour
    if hour > 12:
        hour = now.hour - 12

    now_hour = Image.open("hangul_clock_base/hour/hour_%s_1000_1500.png" % (hour))
    four = alpha_composite(now_hour, three)

    now_minute = Image.open("hangul_clock_base/minute/minute_%s_1000_1500.png" % (now.minute))
    five = alpha_composite(now_minute, four)
 
    result = five

    result.save(filename)

    log_actvity("I completed rendering Clock Render")

    os.remove('clock_rendering.rtl')

    return filename