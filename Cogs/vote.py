
import discord
from discord import Integration, SelectOption
from discord.ui import Button, View, Select
from discord.ext import commands

idlist = [596708010768990209, 587545300126924810, 709533146034602084, 783579362062630933, 825639467494539279,
          829166944946094120]
#               예준                 널                  러마               란토                 덴                 pb봇
client = None
class vote(commands.Cog, name="vote"):
    voting = False
    voter = []
    count = 0
    usid = 0
    re = []
    options = []
    def __init__(self, client: commands.Bot) -> None:
        self.client = client



    @commands.Cog.listener()
    async def on_message(self, message):
        global voting
        global count
        global voter
        global usid
        global re
        global options
        async def callback(interaction):
            if not interaction.user.id in voter:
                voter.append(interaction.user.id)
                await interaction.response.send_message(f"{len(voter)}명 투표")
                re[options.index(selectmenu.values[0])] +=1

            else:
                await interaction.response.defer()
                if interaction.user.dm_channel:
                    await interaction.user.dm_channel.send("중복투표는 불가능하며 수정또한 불가능합니다.")
                elif interaction.user.dm_channel is None:
                    channel = await interaction.user.create_dm()
                    await channel.send("중복투표는 불가능하며 수정또한 불가능합니다.")

        if message.content =="vote end":
            if voting and usid == message.author.id:
                voting = False
                biggest = -1
                embed = discord.Embed(
                    title="투표 결과",
                    color=0xffffff)

                for i in range(0,len(re)-1):
                    if re[i]>biggest:
                        biggest = re[i]
                for i in range(0,len(re)-1):
                    if biggest==re[i]:
                        embed.add_field(name=f"{re[i]}표",value=f"{options[i]}",inline=False)

                for i in range(0,len(re)-1):
                    if not biggest==re[i]:
                        embed.add_field(name=f"{re[i]}표",value=f"{options[i]}",inline=False)
                embed.add_field(name=f"기권", value=f"{re[len(re)-1]}표", inline=False)
                options = []

                await message.channel.send(embed=embed)

        elif message.content.startswith("vote"):
            if str.isdigit(message.content.split(" ")[1]):
                if int(message.content.split(" ")[1]) > 1 and int(message.content.split(" ")[1]) < 10:
                    count = int(message.content.split(" ")[1])
                    if len(message.content[7:].split("/")) == count:
                        options = []
                        voting = True
                        voter = []
                        re = []
                        view = View()
                        selectmenu = Select()
                        for i in range(1, count+1):
                            selectmenu.options.append(SelectOption(label=f"{i}번",description=message.content[7:].split("/")[i - 1]))
                            options.append(message.content[7:].split("/")[i - 1])
                            re.append(0)
                        selectmenu.options.append(SelectOption(label=f"{count+1}번", description="기권"))
                        re.append(0)
                        selectmenu.callback = callback
                        view.add_item(selectmenu)

                        await message.channel.send("*선택 후에는 수정되지 않습니다.", view=view)
                        usid = message.author.id


async def setup(client: commands.Bot) -> None:
    await client.add_cog(vote(client),)
    client = client
