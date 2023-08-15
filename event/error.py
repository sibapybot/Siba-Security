import discord
from discord.ext import commands
import settings
from Logger import Logger
logger = Logger()


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
        guilds=[discord.Object(id=settings.GUILD_ID)]
    )
    logger.info("Error event is ready!")
