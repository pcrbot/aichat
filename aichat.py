import os
import asyncio
import time
import json
import traceback
import nonebot
import random
import threading 
import re
import string
from hashlib import md5
from time import time
from urllib.parse import quote_plus
import aiohttp
from nonebot import get_bot
from nonebot.helpers import render_expression
from hoshino import Service, priv
from hoshino.typing import CQEvent, MessageSegment
from hoshino.modules.aichat import Config
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
#from hoshino.service import Service, Privilege as Priv
sv = Service('人工智障')


SecretId = '' #  填你的SecretId
SecretKey = ''#  填你的SecretKey


try:
    import ujson as json
except ImportError:
    import json

bot = get_bot()
cq_code_pattern = re.compile(r'\[CQ:\w+,.+\]')
salt = None
FILE_FOLDER_PATH = './hoshino/modules/aichat/'
CONFIG_PATH =  f'{FILE_FOLDER_PATH}config.json'
ai_chance = Config(CONFIG_PATH)
DEFAULT_AI_CHANCE = 5   # 默认的AI回复概率

# 定义无法获取回复时的「表达（Expression）」
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～',
    '唔……等会再告诉你'
)



def rand_string(n=8):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(n))


@sv.on_prefix(('调整AI概率'))
async def enable_aichat(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '请联系群管理调整AI概率哦~')
    s = ev.message.extract_plain_text()
    if s:
        if s.isdigit() and 0<int(s)<51:
            chance = int(s)
        else:
            await bot.finish(ev, '参数错误: 请输入1-50之间的整数.')
    else:
        chance = DEFAULT_AI_CHANCE     # 后面不接数字时调整为默认概率
    ai_chance.set_chance(str(ev.group_id), chance)
    await bot.send(ev, f'人工智障已启用, 当前bot回复概率为{chance}%.')


@sv.on_fullmatch(('消除AI概率', '关闭人工智障'))
async def disable_aichat(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '请联系群管理关闭此功能哦~')
    ai_chance.delete_chance(str(ev.group_id))
    await bot.send(ev, f'人工智障已禁用')


@sv.on_message('group')
async def ai_reply(bot, context):   
    msg = str(context['message'])
    if msg.startswith(f'[CQ:at,qq={context["self_id"]}]'):
        text = re.sub(cq_code_pattern, '', msg).strip()
        if text == '':
            return
        try: 
            cred = credential.Credential(SecretId, SecretKey) 
            httpProfile = HttpProfile()
            httpProfile.endpoint = "nlp.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

            req = models.ChatBotRequest()
            params = {
                "Query": text,
            }
            req.from_json_string(json.dumps(params))

            resp = client.ChatBot(req)
            param = resp.to_json_string()
            reply = json.loads(param)
            msg = reply['Reply']
            await bot.send(context, msg,at_sender=False) 
                

        except TencentCloudSDKException as err: 
            print(err) 
        return
    if str(context.group_id) in ai_chance.chance:
        if not random.randint(1,100) <= int(ai_chance.chance[str(context.group_id)]):
            return
        else:           
            text = re.sub(cq_code_pattern, '', msg).strip()
            if text == '':
                return
            try: 
                cred = credential.Credential(SecretId, SecretKey) 
                httpProfile = HttpProfile()
                httpProfile.endpoint = "nlp.tencentcloudapi.com"

                clientProfile = ClientProfile()
                clientProfile.httpProfile = httpProfile
                client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

                req = models.ChatBotRequest()
                params = {
                    "Query": text,
                }
                req.from_json_string(json.dumps(params))

                resp = client.ChatBot(req)
                param = resp.to_json_string()
                reply = json.loads(param)
                msg = reply['Reply']
                await bot.send(context, msg,at_sender=False) 
                

            except TencentCloudSDKException as err: 
                print(err) 
    else:
        return
