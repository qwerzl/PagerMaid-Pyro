import os

from coloredlogs import ColoredFormatter
from logging import getLogger, StreamHandler, ERROR, INFO, basicConfig
from datetime import datetime
from os import getcwd, sep, mkdir
from os import path as os_path
from sqlitedict import SqliteDict
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pagermaid.config import Config
import pyromod.listen
from pyrogram import Client

# init folders
if not os_path.exists("data"):
    os.mkdir("data")

CMD_LIST = {}
module_dir = __path__[0]
working_dir = getcwd()
help_messages = {}
sqlite = SqliteDict(f"data{sep}data.sqlite", autocommit=True)
scheduler = AsyncIOScheduler()
if not scheduler.running:
    scheduler.configure(timezone="Asia/ShangHai")
    scheduler.start()
logs = getLogger(__name__)
logging_format = "%(levelname)s [%(asctime)s] [%(name)s] %(message)s"
logging_handler = StreamHandler()
logging_handler.setFormatter(ColoredFormatter(logging_format))
root_logger = getLogger()
root_logger.setLevel(ERROR)
root_logger.addHandler(logging_handler)
basicConfig(level=INFO)
logs.setLevel(INFO)

# easy check
if not Config.API_ID:
    logs.error("Api-ID Not Found!")
    exit(1)
elif not Config.API_HASH:
    logs.error("Api-Hash Not Found!")
    exit(1)

start_time = datetime.utcnow()
bot = Client("pagermaid", api_id=Config.API_ID, api_hash=Config.API_HASH, ipv6=Config.IPV6)


async def log(message):
    logs.info(
        message.replace('`', '\"')
    )
    if not Config.LOG:
        return
    await bot.send_message(
            Config.LOG_ID,
            message
    )