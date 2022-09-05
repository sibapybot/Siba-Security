import discord
from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(event, *args, **kwargs):
        print(args)
        print(kwargs)
    

    


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Error(bot),
        guilds =[discord.Object(id=964656515686465608)]
    )
    print("errorイベント")