from flask import Flask, Response, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
from datetime import datetime
import os
import string
import random
import time
import random
import json


global bot
global TOKEN
users = []
group_codes = []
TOKEN = os.environ.get('BITS_SECRET_SANTA_TOKEN')
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)


@app.route('/users', methods=['POST'])
def import_users():
    users_json = request.get_json()
    if "users" in users_json:
        global users
        users = users_json["users"]
        return "Ok", 200
    else:
        return "key 'users' not found", 400

@app.route('/groups', methods=['POST'])
def import_groups():
    group_json = request.get_json()
    if "groups" in group_json:
        global group_codes
        group_codes = group_json["groups"]
        return "Ok", 200
    else:
        return "key 'groups' not found", 400


@app.route('/users', methods=['GET'])
def get_users():
    try:
        new_users = users
        return Response(json.dumps({"users": random.sample(new_users, len(new_users))}), mimetype='application/json')
    except:
        return "", 404

@app.route('/groups', methods=['GET'])
def get_groups():
    try:
        return Response(json.dumps({"groups": group_codes}), mimetype='application/json')
    except:
        return "", 404


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    __write_log("chat_id: " + str(chat_id) + " msg_id: " + str(msg_id))

    if update.message.text is not None:

        text = update.message.text.encode('utf-8').decode()

# WELCOME MESSAGE
        if text == "/start":
            bot_welcome = "Ho! Ho! Ho!" + "\n" + "Willkommen beim diesjärigen B!TS Secret Santa Event! Wenn du eine neue Ziehung beginnen willst dann sende /init !"
            bot.sendMessage(chat_id=chat_id, text=bot_welcome,reply_to_message_id=msg_id)

# INIT DRAWING
        elif text.startswith("/init"):
            group_code = __get_random_string(6)
            while group_code in group_codes:
                group_code = __get_random_string(6)
            group_codes.append(group_code)
            init_msg="Euer Gruppencode ist " + group_code + ". Bitte sendet mir privat (@BitsSecretSantaBot) das Kommando /join " + group_code + " wenn ihr teilnehmen wollt."
            bot.sendMessage(chat_id=chat_id, text=init_msg, reply_to_message_id=msg_id)

# JOIN GROUP
        elif text.startswith("/join"):
            if update.message.chat.type != "private":
                bot.sendMessage(chat_id=chat_id, text="Bitte sende mir privat, dass du joinen willst! (@BitsSecretSantaBot)", reply_to_message_id=msg_id)
                return "ok"

            gc = text.strip()[6:]
            if len(gc) < 1:
                bot.sendMessage(chat_id=chat_id, text="Bitte vergiss nicht den Gruppencode beim /join <Gruppencode> Kommando!", reply_to_message_id=msg_id)
                return "ok"
            
            if gc not in group_codes:
                bot.sendMessage(chat_id=chat_id, text="Ich habe keine Gruppe mit dem Code " + str(gc) + " gefunden.", reply_to_message_id=msg_id)
                return "ok"

            for user in users:
                if user['uid'] == update.effective_user.id and gc == user["groupId"]:
                    bot.sendMessage(chat_id=chat_id, text="Du bist bereits in der Gruppe, " + str(update.effective_user.first_name) + "!", reply_to_message_id=msg_id)
                    return "ok"

            __add_user(update.effective_user.id, update.effective_user.first_name, False, gc)
            msg = "Willkommen in der Gruppe, " + str(update.effective_user.first_name) + "!"
            bot.sendMessage(chat_id=chat_id, text=msg)


# SHOW PARTICIPATING USERS
        elif text == ("/users"):
            bot.sendMessage(chat_id=chat_id, text=users)


# SHUFFLE
        elif text.startswith("/shuffle"):
            groupId = text.strip()[9:]
            shuffle_users = []

            if len(groupId)<1:
                bot.sendMessage(chat_id=chat_id, text="Bitte gebe auch eine Gruppen Id ein!", reply_to_message_id=msg_id)
                return 'ok'

            if groupId not in group_codes:
                bot.sendMessage(chat_id=chat_id, text="Ich habe keine Gruppe mit dem Code " + str(groupId) + " gefunden.", reply_to_message_id=msg_id)
                return "ok"  

            rand_users = random.sample(users, len(users))

            for user in rand_users:
                if user["groupId"] == groupId:
                    shuffle_users.append(user)
            
            if len(shuffle_users) < 2:
                bot.sendMessage(chat_id=chat_id, text="Es nehmen aktuell weniger als 2 Leute teil!", reply_to_message_id=msg_id)
                return 'ok'
            
            user_relations = []
            d20_random = len(shuffle_users)

            while(d20_random % len(shuffle_users) == 0):
                d20_random = random.randrange(19)+1

            for i in range(len(shuffle_users)):
                partner_index = (i+d20_random)%len(shuffle_users)
                user_relations.append((shuffle_users[i], shuffle_users[partner_index]))

            __write_log(str(user_relations))

            # VALIDITY CHECK
            val_list_0 = []
            val_list_1 = []
            
            for p in user_relations:
                val_list_0.append(str(p[0]['uid']))
                val_list_1.append(str(p[1]['uid']))

            if not( len(val_list_0) == len(set(val_list_0)) and len(val_list_1) == len(set(val_list_1)) and len(val_list_0) == len(val_list_1) ):
                try:
                    bot.sendMessage(chat_id=chat_id, text="Bei der Auslosung ist etwas schiefgelaufen.")
                    return 'not ok'
                except telegram.TelegramError:
                    return 'not ok'
                    
            # SEND OUT MESSAGES
            for pair in user_relations:
                time.sleep(0.5)
                try:
                    bot.sendMessage(chat_id=str(pair[0]['uid']), text="Die Auslosung ist abgeschlossen. Der D20 ist gerollt! Du darfst " + str(pair[1]['name']) + " beschenken!")
                except telegram.TelegramError:
                    bot.sendMessage(chat_id=chat_id, text=str(pair[0]["name"]) + " konnte nicht angeschrieben werden.")
            bot.sendMessage(chat_id=chat_id, text="Die Auslosung ist abgeschlossen. Alle Teilnehmer sollten eine Nachricht erhalten haben.")

        else:
            return "ok"
    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN), allowed_updates=[
                       "message", "callback_query", "update_id"])
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/unset_webhook', methods=['GET', 'POST'])
def unset_webhook():
    s = bot.deleteWebhook()
    if s:
        return "webhook deletion ok"
    else:
        return "webhook deletion failed"



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
    users.append(dict({"uid": uid, "name": name, "isAdmin": isAdmin, "groupId": groupId}))


def __get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
