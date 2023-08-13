# メインエントリポイント

# discord.pyのインポート
import discord
from discord.ext import commands
# tokenなどの設定のインポート
import settings

cogs = ["cogs.test", "cogs.user", "event.join",
        "event.messagev20", "event.guildjoin"]


class SibaBot(commands.Bot):
    """
    Discord.pyのBot定義ポイントです。
    """
    def __init__(self):
        super().__init__(
            command_prefix="s!",
            intents=discord.Intents.all(),
            application_id=settings.DISCORD_APP_ID
        )
        self.version = "0.1.2β"
        self.admin_user: list[int] = settings.ADMIN_USER  # type: ignore

    async def setup_hook(self) -> None:
        for i in range(len(cogs)):
            await self.load_extension(cogs[i])
        await bot.tree.sync(
            guild=discord.Object(id=int(settings.GUILD_ID)))  # type: ignore

    async def on_ready(self):
        print(f"{self.user}がdiscordに接続しました。")


bot = SibaBot()

# Botを実行するコマンド。
# 下のtype:のコメはインラインコメなので消去厳禁
bot.run(settings.DISCORD_TOKEN)  # type: ignore
