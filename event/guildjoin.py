import discord
from discord.ext import commands
import settings
from Logger import Logger
logger = Logger()


class Guildjoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"{guild.name}に導入されました。")
        embed = discord.Embed(title="芝-セキュリティBOTを導入していただきありがとうございます。",
                              description=f"このBOTのバージョンは{self.bot.version}です。")
        embed.add_field(
            name="バグや不具合について",
            value="このBOTはまだ開発中です。バグなどが多数あると思います。"
            + "\nもし、おかしな挙動などが有りましたら下記のサポートサーバーまでお願いします。")
        embed.add_field(name="BOTのサーポート",
                        value="https://discord.gg/TbTZcpF3qz")
        await guild.system_channel.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Guildjoin(bot),
        guilds=[discord.Object(id=int(settings.GUILD_ID))]  # type: ignore
    )
    logger.info("Guild join event is ready!")
