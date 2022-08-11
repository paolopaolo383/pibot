import os
import async_timeout
import asyncio
from discord import Intents, app_commands
import discord
import random
import json
import numpy
from discord.ext import commands

import main
import token2

files = os.listdir("Cogs")

manager = [596708010768990209, 587545300126924810, 783579362062630933]
idlist = [596708010768990209, 587545300126924810, 709533146034602084, 783579362062630933, 825639467494539279,
          829166944946094120]
#               예준                 널                  러마               란토                 덴                 pb봇
prefix = ""
intents = Intents.default()
intents.message_content = True


class pi(commands.Bot):
    def __init__(self):

        super().__init__(
            command_prefix='/',
            intents=intents,
            sync_command=True,
            application_id=881498177700773889
        )
        self.initial_extension = []

    async def setup_hook(self):
        await client.tree.sync()

    async def on_ready(self):
        global trash
        global files
        await pi.log(self, "봇 시작")
        print("================")
        files = []
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                try:
                    await client.load_extension(f"Cogs.{filename[:-3]}")
                    files.append(filename)
                    print(f"--{filename} 완료")
                except Exception:
                    print(f"--{filename} 실패")
        print("Cogs 로드 완료")
        print("================")

    async def log(self, content):
        await client.get_channel(994181446799466506).send(content + "<:__:927935688509390858>")

    async def sendembed(self, message):
        # loadbtn = Button(label= "Load",style=discord_components.ButtonStyle.red)
        # unloadbtn = Button(label="Unload", style=discord_components.ButtonStyle.green)
        # view = View()
        global files

        l = []
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                l.append(filename)
        if len(l) == len(files):
            embed = discord.Embed(title=" ", color=0x25f105)
        else:
            embed = discord.Embed(title=" ", color=0xff0000)
        for file in l:
            if file.endswith(".py"):
                if not file in files:
                    embed.add_field(name=f"{file[:-3]}", value="❌", inline=True)
                    # view.add_item(loadbtn)

        for f in files:
            embed.add_field(name=f"{f[:-3]}", value="✅", inline=True)
            # view.add_item(unloadbtn)
        # if len(files) ==0:
        #    embed.add_field(name="❌",value="플러그인이 없습니다")
        await message.channel.send(embed=embed)

    @app_commands.command(name="load")
    async def load(self, ctx):
        await ctx.send("a")

    async def on_message(self, message):
        global idlist
        global manager
        global files
        if message.author.bot:
            return
        if not message.author.id in manager:
            return
        if message.content == prefix + "reload all":
            for filename in files:
                await client.unload_extension(f"Cogs.{filename[:-3]}")
                print(f"--{filename} 언로드 완료")

            files = []
            for filename in os.listdir("Cogs"):
                if filename.endswith(".py"):
                    files.append(filename)
            for filename in files:
                await client.load_extension(f"Cogs.{filename[:-3]}")
                print(f"--{filename} 로드 완료")

            await pi.sendembed(self, message)
            await pi.log(self, f"{message.author.name}-reload all")
            return
        if message.content.startswith(prefix + "load "):
            if not len(message.content.split(" ")) == 2:
                await message.channel.send("인자는 1개만 설정 가능합니다")
                return
            else:
                if not message.content.split(" ")[1] + ".py" in os.listdir("Cogs"):
                    await message.channel.send("파일이 없습니다")
                    return
                file = message.content.split(" ")[1] + ".py"
                if file in files:
                    await client.unload_extension(f"Cogs.{file[:-3]}")
                    files.remove(file)
                await client.load_extension(f"Cogs.{file[:-3]}")
                files.append(file)
                await pi.sendembed(self, message)
                print(f"--{file} 로드 완료")
                await pi.log(self, f"{message.author.name}-load all")
                return
        if message.content.startswith(prefix + "unload "):
            if not len(message.content.split(" ")) == 2:
                await message.channel.send("인자는 1개만 설정 가능합니다")
                return
            else:
                if not message.content.split(" ")[1] + ".py" in files:
                    await message.channel.send("파일이 없습니다")
                    return
                file = message.content.split(" ")[1] + ".py"
                await client.unload_extension(f"Cogs.{file[:-3]}")
                files.remove(file)
                await pi.sendembed(self, message)
                print(f"--{file} 언로드 완료")
                await pi.log(self, f"{message.author.name}-unload all")
            return
        if message.content == "plugins":
            await pi.sendembed(self, message)


client = pi()
client.run(token2.gettoken())
