import discord
from discord.ext import commands 

cogs=["cogs.test","cogs.user","event.join","event.messagev20","event.guildjoin"]

class SibaBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!s",
            intents=discord.Intents.all(),
            application_id = 984416937188687883
            )
        self.version = "0.1.2β"
        self.admin_user:list[int]=[843343559965016096,962953982618259476]

    async def setup_hook(self) -> None:
        for i in range(len(cogs)):
            await self.load_extension(cogs[i])
        await bot.tree.sync(guild= discord.Object(id=964656515686465608))

    async def on_ready(self):
        
        print(f"{self.user}がdiscordに接続しました。")

bot = SibaBot()
bot.run("")#てすbot