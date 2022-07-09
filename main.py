import os
import async_timeout
import asyncio
import discord
import random
import json
import numpy
from discord.ext import commands

files = os.listdir("Cogs")
client = commands.Bot(command_prefix=None, help_command=None)
manager = [596708010768990209, 587545300126924810, 783579362062630933]
idlist = [596708010768990209, 587545300126924810, 709533146034602084, 783579362062630933, 825639467494539279,
          829166944946094120]
#               예준                 널                  러마               란토                 덴                 pb봇
prefix = ""


@client.event
async def on_ready():
    global trash
    global files
    await log("봇 시작")
    print("================")
    files = []
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            try:
                client.load_extension(f"Cogs.{filename[:-3]}")
                files.append(filename)
                print(f"--{filename} 완료")
            except Exception:
                print(f"--{filename} 실패")
    print("Cogs 로드 완료")
    print("================")


async def log(content):
    await client.get_channel(994181446799466506).send(content + "<:__:927935688509390858>")


async def sendembed(message):
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

    for f in files:
        embed.add_field(name=f"{f[:-3]}", value="✅", inline=True)
    # if len(files) ==0:
    #    embed.add_field(name="❌",value="플러그인이 없습니다")
    await message.channel.send(embed=embed)


@client.event
async def on_message(message):
    global idlist
    global manager
    global files
    if message.author.bot:
        return
    if not message.author.id in manager:
        return
    if message.content == prefix + "reload all":
        for filename in files:
            client.unload_extension(f"Cogs.{filename[:-3]}")
            print(f"--{filename} 언로드 완료")

        files = []
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                files.append(filename)
        for filename in files:
            client.load_extension(f"Cogs.{filename[:-3]}")
            print(f"--{filename} 로드 완료")

        await sendembed(message)
        await log(f"{message.author.name}-reload all")
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
                client.unload_extension(f"Cogs.{file[:-3]}")
                files.remove(file)
            client.load_extension(f"Cogs.{file[:-3]}")
            files.append(file)
            await sendembed(message)
            print(f"--{file} 로드 완료")
            await log(f"{message.author.name}-load all")
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
            client.unload_extension(f"Cogs.{file[:-3]}")
            files.remove(file)
            await sendembed(message)
            print(f"--{file} 언로드 완료")
            await log(f"{message.author.name}-unload all")
        return
    if message.content == "plugins":
        await sendembed(message)


client.run("ODgxNDk4MTc3NzAwNzczODg5.GHP9cH.wGPxO1CDTo8z8NWRFsHm4WyfYDTmNOuXTyLeYI")
