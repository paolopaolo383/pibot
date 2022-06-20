from unicodedata import name
import discord
from discord.ext import commands
import json

class basic(commands.Cog):
    """
    가장 기본적인 명령어들이 모여있는 카테고리 입니다.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.id==709533146034602084:
            return
        #await message.channel.send("어쩔티비")




def setup(client):
    client.add_cog(basic(client))
