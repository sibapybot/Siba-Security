
import discord
import cv2
import csv
import numpy as np
import requests
import difflib

path_csv = r"C:\Users\waon-pc\Desktop\sibainu_discord\siba_bot\data\avater_img.csv"


def dl_file(url, dst_path):

    response = requests.get(url)
    image = response.content

    with open(dst_path, "wb") as f:
        f.write(image)
    return True


def csv_read(guild_id):
    try:
        with open(rf"C:\Users\waon-pc\Desktop\sibainu_discord\siba_bot\data\avater{guild_id}_img.csv", "r") as f:
            reader = csv.reader(f)
            list = [row for row in reader]
            return list[0]
    except FileNotFoundError:
        return []


def csv_write(data: list, guild_id):
    with open(rf"C:\Users\waon-pc\Desktop\sibainu_discord\siba_bot\data\avater{guild_id}_img.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(data)


async def avatar_check(member):
    user, guild = member, member.guild
    name, user_id, avatar_url, guild_id = user.name, user.id, user.avatar, guild.id
    name = discord.utils.get(guild.members, name=f"{name}")
    path = fr"C:\Users\waon-pc\Desktop\sibainu_discord\siba_bot\data\avatar_img\{user_id}.png"

    if avatar_url is not None:  # デフォルトのアバターはパスする
        avatar_url = avatar_url.url
        s = dl_file(url=avatar_url, dst_path=path)
        if s:
            lists = list(csv_read(guild_id=guild_id))
            img_avatar_now = cv2.imread(path)
            for i in range(len(lists)):

                img__avatar_old = cv2.imread(
                    fr"C:\Users\waon-pc\Desktop\sibainu_discord\siba_bot\data\avatar_img\{lists[i]}.png")
                if np.array_equal(img_avatar_now, img__avatar_old):  # アバターが一致する場合

                    if int(lists[i]) != int(user_id):  # 自分のアバターはパスする
                        return 1

                    else:  # 自分のアバター
                        return 2

        else:  # アバターのダウンロードに失敗しました。
            return 5

    else:  # デフォルトアバター
        return 4

    lists.append(user_id)
    csv_write(data=lists, guild_id=guild_id)
    return 3  # 一致なし


async def name_check(guild) -> list:
    """
    サーバーの全てのメンバーを取得する
    """
    return [i.name for i in guild.members]


def message_approximate(message_list: list, id_message_list: list) -> list:
    """
    近似
    出力↓
    最後は全てのメッセージの近似
    それ以外は個別のメッセージの近似
    例：[message.ave,message.ave,message.ave,all_message_ave]
    """
    message_ave: list = []
    all_message_ave: list = []
    for z in range(len(message_list)):
        for i in range(len(message_list)):
            if id_message_list[z] != id_message_list[i]:

                message_ave.append(difflib.SequenceMatcher(
                    None, message_list[z], message_list[i]).ratio())

        all_message_ave.append(np.average(message_ave))

        message_ave.clear()
    all_message_ave.append(np.average(all_message_ave))
    return all_message_ave
