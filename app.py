from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
from datetime import datetime
import json
import os
from wichtel_service import WichtelService
import string
import random


global bot
global TOKEN
users = json.dumps(dict({'users': []}), indent=4)
group_codes = []
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
secret_santa_service = WichtelService()

app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    __write_log("chat_id: " + str(chat_id) + " msg_id: " + str(msg_id))

    if hasattr(update, "message"):

        text = update.message.text.encode('utf-8').decode()

        # Welcome message
        if text == "/start":
            group_code = __get_random_string(6)
            while group_code in group_codes:
                group_code = __get_random_string(6)
            bot_welcome = "Ho! Ho! Ho!" + "\n" + "Willkommen beim diesjärigen B!TS Secret Santa Event! Euer Gruppen Code ist '" + \
                group_code + "'" + "\n" + "Bitte sendet mir per Direktnachricht '/join " + \
                group_code + "', um teilzunehmen."

            bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                            reply_to_message_id=msg_id)

            bot.sendMessage(chat_id=chat_id, text=str(update.message),
                            reply_to_message_id=msg_id)

        # Join group
        elif text.startswith("/join"):
            if update.message.chat.type == "private":
                gc = text.strip()[6:]
                __add_user(update.effective_user.id, update.effective_user.first_name, False, gc)
                msg = "Willkommen in der Gruppe!"
                bot.sendMessage(chat_id=chat_id, text=msg)
            else:
                bot.sendMessage(chat_id=chat_id, text="Bitte sende mir deinen Gruppenbeitritt privat!", reply_to_message_id=msg_id)
            bot.sendMessage(chat_id=chat_id, text=str(update.message), reply_to_message_id=msg_id)
        
        elif text == ("/users"):
            bot.sendMessage(chat_id=chat_id, text=users)

        elif text.startswith("/shuffle"):
            group_name = text.strip()[9:]
            print("group: " + str(group_name))
            shuffle_users = []
            dict_users = json.loads(users)
            print("dict_users: " + str(dict_users))

            for user in dict_users["users"]:
                if user == group_name:
                    shuffle_users.append(user)
            
            user_relations = []
            d20_random = len(users)

            while(d20_random % len(users) == 0):
                d20_random = random.randrange(19)+1

            for i in range(len(users)):
                partner_index = (i+d20_random)%len(users)
                user_relations.append((users[i], users[partner_index]))
            
            for relation in user_relations:
                send_user = json.loads(relation[1])
                bot.sendMessage(chat_id=chat_id, text="Du darfts " + send_user["name"] + " beschenken!")

    
        

        else:
            try:
                bot.sendMessage(
                    chat_id=chat_id, text="I received your message", reply_to_message_id=msg_id)
            except Exception:
                # if things went wrong
                bot.sendMessage(
                    chat_id=chat_id, text="I received your message", reply_to_message_id=msg_id)
    print(str(message))
    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN), allowed_updates=[
                       "message", "callback_query", "update_id"])
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
    log = "\n" + \
        str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " - " + msg
    file.write(log)
    file.close()


def __add_user(uid, name, isAdmin, groupId):
    global users
    dict_users = json.loads(users)
    dict_users["users"].append(
        dict({"id": uid, "name": name, 'isAdmin': isAdmin, 'groupId': groupId}))
    users = json.dumps(dict_users, indent=4)


def __get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
