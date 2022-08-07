
import discord
from discord.ext import commands

class basic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "help" or message.content == "invite":
            embed = discord.Embed(
                title="PI BOT",
                description="3.141592653589793238462643383279502884197169399375105820974944...",
                color=0xffffff)
            embed.add_field(name="PI초대",value="[봇 초대](https://discord.com/api/oauth2/authorize?client_id=881498177700773889&permissions=8&scope=bot)",inline=True)
            embed.add_field(name="PI봇 Github",
                            value="[Github 링크](https://github.com/paolopaolo383/pibot)",
                            inline=True)

            await message.channel.send(embed=embed)




def setup(client):
    client.add_cog(basic(client))
