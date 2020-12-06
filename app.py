from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL
from datetime import datetime
import json
import os
from wichtel_service import WichtelService

global bot
global TOKEN
users = json.dumps(dict({'users': []}), indent=4)
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
secret_santa_service = WichtelService()

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)
   print(update.message)
   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   __write_log("chat_id: " + str(chat_id) + " msg_id: " + str(msg_id))

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # Welcome message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Ho! Ho! Ho!
       Willkommen beim diesjärigen B!TS Secret Santa Event! Wenn du teilnehmen möchtest dann sende /join !
       Ho! Ho! Ho!
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)


   else:
       try:
           bot.sendMessage(chat_id=chat_id, text="I received your message", reply_to_message_id=msg_id)
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="I received your message", reply_to_message_id=msg_id)

   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN), allowed_updates=["message", "callback_query", "update_id"])
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"


def __write_log(msg):
    filename = 'logs.txt'
    if os.path.exists(filename):
        file_mode = 'a'
    else:
        file_mode = 'w+'
    file = open(filename, file_mode)
    log = "\n" + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " - " + msg
    file.write(log)
    file.close()


def __add_user(name, isAdmin, groupId):
    global users
    dict_users = json.loads(users)
    dict_users["users"].append(dict({"name": name, 'isAdmin': isAdmin, 'groupId': groupId}))
    users = json.dumps(dict_users, indent=4)  


if __name__ == '__main__':
   app.run(host='0.0.0.0', threaded=True)
