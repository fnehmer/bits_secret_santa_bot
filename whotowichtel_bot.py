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
from models.wichtel_room import WichtelRoom
from util import get_random_string
from wichtel_service import WichtelService

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger(__name__)

# Settings
bot_token = os.getenv('WHOTOWICHTEL_BOT_TOKEN', '')
wichtel_service = WichtelService()
wichtel_service.load_state()


def start_command(update, context):
    telegram_user = TelegramUser.from_telegram_user_object(update.message.from_user)
    reply = "Ho Ho Ho {}".format(telegram_user.first_name)
    update.message.reply_text(reply)


def create_command(update, context):
    code = get_random_string(6)
    telegram_user = TelegramUser.from_telegram_user_object(update.message.from_user)

    reply = 'Your group has been created. Use this token to invite your friends:\n%s\n' % code
    wichtel_room = WichtelRoom(
        code=code,
        admin_user=telegram_user,
        telegram_users=[]
    )

    wichtel_service.wichtel_rooms.append(wichtel_room)
    wichtel_service.save_state()
    update.message.reply_text(reply)


def join_command(update, context):
    if not context.args:
        reply = 'Please enter the code wichtel-room you would like to join like that:\n\n /join <code>'
        update.message.reply_text(reply)
        return

    code = context.args[0]
    telegram_user = TelegramUser.from_telegram_user_object(update.message.from_user)
    wichtel_room = wichtel_service.add_user_to_group(telegram_user, code)
    if wichtel_room:
        reply = 'You joined the Wichtel-Group of {}!'.format(wichtel_room.admin_user.first_name)
        update.message.reply_text(reply)
    else:
        reply = 'Code "{}" seems to be invalid! :('.format(code)
        update.message.reply_text(reply)


def help_command(update, context):
    reply = "Enter /create to create a new room. Your old room will not be deleted.\
    \nEnter /join to join an existing room."
    update.message.reply_text(reply)


def repeat(update, context):
    update.message.reply_text(update.message.text)
    telegram_user = TelegramUser.from_telegram_user_object(update.message.from_user)


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
