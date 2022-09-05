import discord
from discord.ext import commands

class Emoji_Role(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        pass




async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Emoji_Role(bot),
        guilds =[discord.Object(id=964656515686465608)]
    )
    print("入室イベント準備OK")