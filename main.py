# メインエントリポイント
from Logger import Logger
# discord.pyのインポート
import discord
from discord.ext import commands
# tokenなどの設定のインポート
import settings

cogs = ["cogs.test", "cogs.user", "event.joinUserCheckerv2",
        "event.messageCheckerV20", "event.guildJoin"]

logger = Logger()
logger.remove_oldlog()
logger._create_log_gitignore()
logger.info("Start main.py")


class SibaBot(commands.Bot):
    """
    Discord.pyのBot定義ポイントです。
    """

    def __init__(self):
        # 親属性の初期化をし、Botの設定をする。
        super().__init__(
            command_prefix="s!",
            intents=discord.Intents.all(),
            application_id=settings.DISCORD_APP_ID
        )
        self.version = "0.2.0β"
        self.admin_user: list[int] = settings.ADMIN_USER  # type: ignore

    async def setup_hook(self) -> None:
        # discordのWSに接続する前にする処理の記述。
        for cog in cogs:
            # コグのロード
            await self.load_extension(cog)
        await bot.tree.sync(
            guild=discord.Object(id=int(settings.GUILD_ID)))  # type: ignore

    async def on_ready(self):
        logger.info(f"Logined as {self.user}.")


bot = SibaBot()
bot.run(settings.DISCORD_TOKEN)
