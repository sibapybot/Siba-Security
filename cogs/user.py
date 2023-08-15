import discord
from discord import app_commands
from discord.ext import commands
from Logger import Logger
import settings
logger = Logger()


class User_Command(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ユーザ情報", description="指定したユーザー情報を確認できます。")
    async def user(self, interaction: discord.Interaction, user_id: str):
        # try:
        user = self.bot.get_user(user_id)

        name = user.name
        color = user.accent_color
        created_at = user.created_at
        avatar = user.display_avatar.url
        user_id = user.id

        embed = discord.Embed(
            title="ユーザー情報", description=f"{name}さんの情報", color=color)
        embed.add_field(name="アカウント作成日",
                        value=f"<t:{int(created_at.timestamp())}>")
        embed.add_field(name="ユーザーID", value=f"`{user_id}`")
        embed.set_thumbnail(url=avatar)
        # except:
        #    　embed = discord.Embed(title="エラー",description="ユーザー情報を取得できませんでした。",color=0xfc2a00)  # noqa

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        User_Command(bot),
        guilds=[discord.Object(id=settings.GUILD_ID)]
    )
    logger.info("Test command is ready!")
