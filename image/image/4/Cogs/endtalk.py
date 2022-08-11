from unicodedata import name
import discord
from discord.ext import commands
import json
import random
import math

idlist = [596708010768990209, 587545300126924810, 709533146034602084, 783579362062630933, 825639467494539279, 829166944946094120]
#               예준                 널                  러마               란토                 덴                 pb봇

class Room:
    def __init__(self, roomid, moderator):
        self.roomid = roomid
        self.player = []
        self.player.append(moderator)




class endtalk(commands.Cog, name="endtalk"):

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    def createroom(self, roomid):
        pass


    async def on_message(self, message):
        pass


async def setup(client: commands.Bot) -> None:
    await client.add_cog(
        endtalk(client),
    )
