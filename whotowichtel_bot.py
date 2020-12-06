#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
from models.telegram_user import TelegramUser

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger(__name__)

# Settings
bot_token = os.getenv('WHOTOWICHTEL_BOT_TOKEN', '')
wichtel_service = None


def start_command(update, context):
    telegram_user = TelegramUser.from_telegram_user_object(update.message.from_user)
    reply = "Ho Ho Ho {}".format(telegram_user.first_name)
    update.message.reply_text(reply)


def create_command(update, context):
    reply = 'You created a group... not. At this point a room code will be returned.'
    update.message.reply_text(reply)


def join_command(update, context):
    reply = 'You joined a room... not. Usually, you will be asked for an existing room code.'
    update.message.reply_text(reply)


def help_command(update, context):
    reply = "Enter /create to create a new room. Your old room will not be deleted.\
    \nEnter /join to join an existing room."
    update.message.reply_text(reply)


def repeat(update, context):
    update.message.reply_text(update.message.text)
    telegram_user = TelegramUser.from_telegram_user_object(update.message.from_user)
    print(telegram_user.to_dict())


def main():
    updater = Updater(bot_token, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("create", create_command))
    dispatcher.add_handler(CommandHandler("join", join_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, repeat))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
