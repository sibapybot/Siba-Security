# Noused
# import asyncio
import discord
from discord.ext import commands
import MeCab
import datetime
from Logger import Logger

logger = Logger()


class User_Join(commands.Cog):
    """
    このイベントは、入室イベントです。
    これはjoin.pyを作り直したものです。
    何かしら一致したユーザーを見つけた場合、承認を待機します。
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def on_message(self, message: discord.message):
        # discordの色々
        member = self.bot.get_member(message.author.id)
        guild = member.guild
        sys_ch = guild.system_channel

        # MeCabをセットする
        m = MeCab.Tagger("-Ochasen")

        embed = discord.Embed(title="スキャンをしています。")
        embed.add_field(name="対象ユーザー", value=f"{member.name}")
        embed.set_thumbnail(url=member.display_avatar.url)
        await sys_ch.send(embed)

        if member.bot:
            embed.add_field(name="結果", value="BOTのためパスしました。")
            return

        tmp_n = [line.split()[0] for line in m.parse(
            member.name).splitlines()
            if "名詞" and "名詞-数" not in line.split()[-1]]
        names = [mbr.name for mbr in guild.members]
        for s in range(len(names)):
            tmp = [line.split()[0] for line in m.parse(names[s]).splitlines()
                   if "名詞" and "名詞-数" not in line.split()[-1]]
            del tmp[-1]
            names[s] = tmp

        for z in names:
            if z == tmp_n:
                embed.add_field(name="名前がほぼ一致いるユーザーがいませんか？",
                                value="対象ユーザーはタイムアウトされます。")
                await member.timeout(datetime.timedelta(days=28))
                logger.debug(f"Timeout:{member} in {guild}")
                break


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        User_Join(bot)
    )
    logger.info("Join users checker v2 is ready!")
