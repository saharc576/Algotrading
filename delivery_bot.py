import logging
import re
from datetime import datetime

import telegram
from jinja2 import (Environment, FileSystemLoader,
                    select_autoescape)
from prometheus_client import CollectorRegistry, Histogram, push_to_gateway
from telegram.parsemode import ParseMode
from telegram.update import Update
from telegram.forcereply import ForceReply
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from config_file import Telegram


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

env = Environment(loader=FileSystemLoader("templates"),
                  autoescape=select_autoescape())

current_users = []
logger = logging.getLogger(__name__)

# set redis to store found sure-bets with timeout
r = RedisConfig.R.value


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    current_users.append(user.id)
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    print(context.chat_data)
    update.message.reply_text("No supporting private chatting...")


def broadcast_message(msg: dict):
    telegram_bot = telegram.bot.Bot(token=Telegram.TOKEN.value)
    payload_to_send = generate_automated_message(msg)

    telegram_bot.send_message(
        chat_id=Telegram.CHAT_ID.value,
        parse_mode=ParseMode.HTML,
        text=payload_to_send)

    print("[Telegram-bot] sent message")


def generate_automated_message(msg: dict):
    template = env.get_template("telegram_message.tpl")
    result = template.render(stock_name=msg["stock_name"], buy_or_sell=msg["buy_or_sell"])

    return result





if __name__ == '__main__':
    start_bot()