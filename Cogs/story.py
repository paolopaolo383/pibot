from unicodedata import name
import discord
from discord.ext import commands
import json
import random
import math

msgchannel = 0
idlist = [596708010768990209, 587545300126924810, 709533146034602084, 783579362062630933, 825639467494539279,
          829166944946094120]


#               예준                 널                  러마               란토                 덴                 pb봇
async def sayrandom(msglist):
    await msgchannel.send(msglist.get(random.randrange(0, len(msglist))))


class story(commands.Cog, name="story"):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.channel.id == 957591309428854824:
            return
        msgchannel = message.channel
        if message.author.id == 709533146034602084:
            if message.content == "야":
                m =["왜", "싫어", "(가볍게 무시)"]
                await sayrandom(m)
            elif "배워하자" in message.content:
                await sayrandom(["싫어", ":__~26:", ":__~28:", "응 안해"])
            elif "스워하자" in message.content:
                await sayrandom(["솔로니까 솔로로해", "싫", "ㄴ", "찮귀"])
            elif "유챔하자" in message.content:
                await sayrandom(["나아아중에 ㄱ", str(random.randrange(2, 40)) + "년 뒤에 하자^^", "ㄴ"])
        if message.content == "ㅇㅎ":
            await sayrandom(["알기는 뭘알어", "ㅋ 지금까진 몰랐냐?", "~~야함~~"])
        elif message.content.endswith(" 해야지"):
            await sayrandom(["가능?", "니가?", "어쩔티비"])
        elif message.content == "저쩔티비":
            await sayrandom(["어쩔코딩"])
        elif message.content == "할거임":
            await sayrandom(["어쩌라는거지", "어쩔티비", "니가?", "가능?"])
        elif message.content == "ㄷ":
            await sayrandom(["e", "ㄷ", "ㄷㄷ", "ㄷ?"])
        elif "ㅠㅠ" in message.content:
            await sayrandom(["ㅋ", "ㅋㅎㅋㅎㅋㅎ"])
        elif "?" in message.content:
            if message.content.endswith("?"):
                await sayrandom(["?", "ㅁ?ㄹ"])
            else:
                await sayrandom(["...?", "?", "??", "???"])


def setup(client):
    client.add_cog(story(client))
