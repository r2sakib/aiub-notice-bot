# python 3.11.4

import os
from telebot import TeleBot
from dotenv import load_dotenv


def send_notice_message(message: str):
    """
    Sends a notice message to a Telegram chat using the Telegram Bot API.

    Args:
        message (str): The message to be sent.

    Returns:
        None
    """
    load_dotenv()
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')

    bot=TeleBot(BOT_TOKEN, parse_mode="HTML")
    bot.send_message(CHAT_ID, message, disable_web_page_preview=True)


def notice_message_formatter(notice_title, notice_link):
    return f'New notice:\n<a href="{notice_link}">{notice_title}</a>'