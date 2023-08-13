from discord.ext import commands
import discord
import asyncio
import re
import msg_ck
import datetime
import time


class MessageV20(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # ここからはメッセージ等の一時的な保管リスト
        self.tmp_message = {}
        # {
        # [message.content,time]
        # }
        self.tmp_guild: dict = {}
        # {
        # guild_id:{
        #           Notification_time:xxxx,
        #           Embed:embed,
        #           guild:guild
        #           slowchannel:[
        #                       [channel,もとのメッセージ速度]
        #                       ],
        #           tmp_m:[
        #                  [message,member,0,時間]#0はすでに処理済みかどうか
        #                  ],
        #           TO_member:[timeout済みのメンバーのIDを記録]
        #           }
        # }

    # メンバーのタイムアウト
    async def member_timeout(self, guild: discord.guild):
        nonecount = 0

        async def m_to(member):
            try:
                await member.timeout(datetime.timedelta(days=28))
            except:  # noqa:E722
                print("何らかの原因でタイムアウトできません")
        # タイムアウトする(今は例外処理は実装しない)
        while nonecount <= 30:
            print(nonecount)
            TOlist = [i[1] for i in self.tmp_guild[guild.id]["tmp_m"]
                      if i[2] == 0 and i[1].id
                      not in self.tmp_guild[guild.id]["TO_member"]]
            if not TOlist:
                nonecount += 1
            else:
                nonecount = 0
                to_list: list = []

                for member in TOlist:
                    self.tmp_guild[guild.id]["TO_member"].append(member.id)
                    to_list.append(m_to(member=member))
                await asyncio.gather(*to_list)

            await asyncio.sleep(1)

        # 荒らしが収まったとき
        # メッセージの削除
        await self.purge_msg(guild.id)
        # 低速モードの解除
        await self.reto_ch(guild.id)

        del self.tmp_guild[guild.id]

    # メッセージ処理
    async def purge_msg(self, guild_id: int):
        print("メッセージ削除開始")
        tmp_m = self.tmp_guild[guild_id]["tmp_m"]
        slowchannel = self.tmp_guild[guild_id]["slowchannel"]

        # チャンネル&ユーザー&limit　指定
        msg_id = [i[0].id for i in tmp_m]
        channel = [i[0] for i in slowchannel]
        print(msg_id)
        for i in channel:
            def check(msg):
                print(msg.content)
                return msg.id in msg_id
            await i.purge(limit=len(tmp_m), check=check)
        embed = discord.Embed(
            title="メッセージの削除が完了しました。",
            description="荒らしと判断したメッセージは削除が完了しました。",
            color=0x00e626)
        await self.tmp_guild[guild_id]["guild"].system_channel.send(
            embed=embed)

    # 低速チャンネルの解除
    async def reto_ch(self, guild_id):
        data = self.tmp_guild[guild_id]
        for ch_data in data["slowchannel"]:
            await ch_data[0].edit(slowmode_delay=ch_data[1])
        embed = discord.Embed(
            title="低速モード解除",
            description="低速モードが自動解除されました。\nもともと低速モードを設定していた場合は元の値に戻りました。",
            color=0x00e626)
        await data["guild"].system_channel.send(embed=embed)

    # メインのトリガー
    # 荒らしが検知されるとここが発火する
    async def embed_create(self,
                           member: discord.member,
                           message: discord.message):
        now = datetime.datetime.now()
        slow = message.channel.slowmode_delay
        guild = message.guild
        # データを格納するところ
        # データが登録されていない場合新しくデータを作る
        print(guild.id in self.tmp_guild)
        if guild.id not in self.tmp_guild:
            embed = discord.Embed(title="荒らしを検知しました。",
                                  description="発言はお控えください。", color=0xe62600)
            emessage = await guild.system_channel.send(embed=embed)
            self.tmp_guild[guild.id] = {
                "Notification_time": now,
                "Embed": emessage,
                "guild": guild,
                "slowchannel": [
                    [message.channel, slow]
                ],
                "tmp_m": [
                    [message, member, 0, now]
                ],
                "TO_member": []
            }
            await message.channel.edit(slowmode_delay=15)
            await self.member_timeout(guild)
        # すでに登録されている場合はデータの追加のみ行う。
        elif guild.id in self.tmp_guild:
            guild_date = self.tmp_guild[guild.id]
            # あらしのデータを追加
            guild_date["tmp_m"].append([message, member, 0, now])
            # 低速モードをつける
            slch = [i[0].id for i in guild_date["slowchannel"]]
            if message.channel.id not in slch:
                guild_date["slowchannel"].append([message.channel, slow])
                await message.channel.edit(slowmode_delay=15)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.content)
        start_time = time.time()

        if message.author.bot:
            return
        if message.author.id in self.bot.admin_user:
            print("開発書は偉い")
            return
        guild: discord.guild = message.guild
        member: discord.member = guild.get_member(message.author.id)

        point: int = 0  # 脅威ポイント

        now = datetime.datetime.now()

        # 文字列の精査(似たような文字列が過去に複数あれば脅威はその分増す。)
        if guild.id in self.tmp_message:
            time_a = datetime.timedelta(
                hours=now.hour, minutes=now.minute, seconds=now.second)
            # 30秒以上経ったメッセージの削除
            to_message: list = []
            for i in range(len(self.tmp_message[guild.id])):
                dt = self.tmp_message[guild.id][i][1]
                total_seconds_a = time_a.total_seconds()
                time_c = datetime.timedelta(
                    hours=dt[3], minutes=dt[4], seconds=dt[5])
                total_seconds_c = time_c.total_seconds()
                if total_seconds_a-total_seconds_c >= 30:
                    to_message.append(i)
            for i in sorted(to_message, reverse=True):
                self.tmp_message[guild.id].pop(i)

            time_c = datetime.timedelta(
                hours=dt[3], minutes=dt[4], seconds=dt[5])
            text_list = [i[0] for i in self.tmp_message[guild.id]
                         if time_a - time_c <= datetime.timedelta(seconds=30)]
            m = msg_ck.TextAnalysis(text_list=text_list[-30:-1])
            text_point: int = m.sentence_w(target_text=message.content)
        else:
            text_point: int = 0
        # print(text_point)
        point += text_point

        # everyoneメンションをすると脅威度が+50
        if message.mention_everyone:
            point += 50

        # メンション1個あたり脅威+20
        #
        # if not not message.mention:
        #    point += len(message.mention)*20

        # 招待リンクを貼ると脅威度が+20
        target = "https://discord.gg/"
        if target in message.content:
            idx = message.content.find(target)
            r = message.content[idx+len(target):]
            re.match("[0-9a-zA-Z]{7,10}", r)
            point += 20

        # トークンを貼ると脅威が+1000
        if re.match(r"[0-9a-zA-Z_\-]{24}.[0-9a-zA-Z_\-]{6}.[0-9a-zA-Z_\-]{27} OR [0-9a-zA-Z_\-]{24}.[0-9a-zA-Z_\-]{6}.[0-9a-zA-Z_\-]{38}", message.content):  # noqa: E501
            point += 1000

        if guild.id not in self.tmp_message:
            self.tmp_message[guild.id] = []
        # メッセージの追加
        self.tmp_message[guild.id].append(
            [message.content,
             [now.year, now.month, now.day, now.hour, now.minute, now.second]])

        time2 = time.time()
        print(point)
        # あらしと検知されたらif分岐
        if point >= 80:
            print("タイムアウト")
            await self.embed_create(member=member, message=message)

            print(f"alltime:{time.time() - start_time}\n{time.time()-time2}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        MessageV20(bot),
        guilds=[discord.Object(id=964656515686465608)]
    )
    print("メッセージチェッカーv2.0準備OK")
