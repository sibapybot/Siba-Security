import discord
from discord import app_commands
from discord.ext import commands
from Logger import Logger
logger = Logger()


class Test_Command(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="テスト",
        description="テストコマンド")
    async def introduce(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="テスト成功", description="テスト成功しました。\nbotは正常に稼働しています。",
            color=0x7cfc00)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Test_Command(bot),
        guilds=[discord.Object(id=964656515686465608)]
    )
    logger.info("User command is ready!")
