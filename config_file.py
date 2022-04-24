from enum import Enum
import os

# TODO: sentiment analyses - link http://telegram.me/algotrading_bgu_bot

os.environ["TOKEN"] = "5222420548:AAEdptyCRjeELRSywHI9V06k3CsH5fWuLiE"
os.environ["CHAT_ID"] = "-1001600351832"

class Telegram(Enum):
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
