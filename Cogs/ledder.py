from unicodedata import name
import discord
from discord.ext import commands
import json




class ledder(commands.Cog, name="ledder"):
    """
    가장 기본적인 명령어들이 모여있는 카테고리 입니다.
    """

    def __init__(self, client):
        self.client = client




def setup(client):
    client.add_cog(ledder(client))
