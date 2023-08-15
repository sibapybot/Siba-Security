# envを使うためのインポート
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
PREFIX = os.environ.get("PREFIX")
DISCORD_APP_ID = os.environ.get("DISCORD_APP_ID")
ADMIN_USER = os.environ.get("ADMIN_USER")
GUILD_ID = os.environ.get("GUILD_ID")
