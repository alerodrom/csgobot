# import pdb
import sys
from importlib import reload

import telebot

from db_helper import DBHelper

############################################
#                 DATOS                    #
############################################
reload(sys)

TOKEN = '309560265:AAGdFVXhRF0qtknpZRQLAtPt04YJo-kWnMs'

bot = telebot.TeleBot(TOKEN)

db = DBHelper()
db.setup()

# test -1001280311618
# CSGO -1001107551770
GROUP_ID = -1001107551770

ADMINS = [6879883, 15418061, 150147251, 258786599]


############################################
#                 FUNCIONES                #
############################################


def get_info(message):
    chat_id = message.chat.id
    file = open('util/info.txt', 'r', encoding='utf-8')
    text = file.read()
    file.close()
    bot.send_message(chat_id, str(text), parse_mode='Markdown')


def echo(message):
    chat_id = message.chat.id
    text = "Hola " + message.from_user.first_name + " has puesto: " + message.text[6:]
    bot.send_message(chat_id, str(text), parse_mode='Markdown')


def create_mix(message):
    chat_id = message.chat.id
    user = message.from_user
    text = str(message.text[12:])
    if chat_id == GROUP_ID and user.id in ADMINS:
        msg = db.create_mix(text)
        bot.send_message(chat_id, msg)
    else:
        message = "No eres admin"
        bot.send_message(chat_id, message)


def in_mix(message):
    chat_id = message.chat.id
    user = message.from_user
    if chat_id == GROUP_ID:
        alias = "@" + user.username if user.username is not None else user.first_name
        db.add_item(str(user.id), str(user.first_name), alias)
        msg = 'Te has añadido correctamente ' + str(alias)
        bot.send_message(chat_id, msg)
    else:
        message = "Este comando solo esta disponible para el grupo de CSGO:NOOBS"
        bot.send_message(chat_id, message)


def out_mix(message):
    chat_id = message.chat.id
    user = message.from_user
    if chat_id == GROUP_ID:
        alias = "@" + user.username if user.username is not None else user.first_name
        db.delete_item(str(user.id))
        msg = 'Te has eliminado correctamente ' + str(alias)
        bot.send_message(chat_id, msg)
    else:
        message = "Este comando solo esta disponible para el grupo de CSGO:NOOBS"
        bot.send_message(chat_id, message)


def list_mix(message):
    chat_id = message.chat.id
    if chat_id == GROUP_ID:
        items = db.get_items()
        print(items)
        bot.send_message(chat_id, items, parse_mode='Markdown')
    else:
        message = "Este comando solo esta disponible para el grupo de CSGO:NOOBS"
        bot.send_message(chat_id, message)


def test(message):
    print("TEST")

def get_javigon(message):
    chat_id = message.chat.id
    bot.send_audio(chat_id=chat_id, audio=open(getfile()))

def get_zen(message):
    chat_id = message.chat.id
    message = "ZEN esta en la MIX"
    bot.send_message(chat_id, message)
    #in_mix(zen)
    user = 'ZeN88'
    if chat_id == GROUP_ID:
        alias = "@" + user.username if user.username is not None else user.first_name
        print(user.id)
        db.add_item(str(user.id), str(user.first_name), alias)
        bot.send_message(chat_id, 'Has añadido correctamente a @ZeN88')
    else:
        message = "Este comando solo esta disponible para el grupo de CSGO:NOOBS"
        bot.send_message(chat_id, message)

############################################
#                 LISTENER                 #
############################################

def listener(messages):
    for message in messages:
        if message.content_type == 'text':
            cid = message.chat.id
            if cid > 0:
                mensaje = str(message.chat.first_name) + " [" + str(cid) + "]: " + message.text
            else:
                mensaje = str(message.from_user.first_name) + "[" + str(cid) + "]: " + message.text
            f = open('log.txt', 'a')
            f.write(mensaje + "\n")
            f.close()
        elif message.content_type == 'new_chat_members':
            for user in message.new_chat_members:
                alias = " (@" + user.username + "). " if user.username is not None else ". "
                welcome = 'Bienvenido *' + str(user.first_name) + "*" + str(alias)
                bot.send_message(message.chat.id, welcome, parse_mode='Markdown')
                get_info(message)


bot.set_update_listener(listener)


############################################
#                 COMANDOS                 #
############################################

@bot.message_handler(commands=['start'])
def command_start(m):
    comando = m.text[7:]
    if comando == 'info':
        get_info(m)


@bot.message_handler(commands=['info'])
def command_z1(m):
    get_info(m)


@bot.message_handler(commands=['echo'])
def command_echo(m):
    echo(m)


@bot.message_handler(commands=['test'])
def command_reply_to_pinned(m):
    test(m)


@bot.message_handler(commands=['create_mix'])
def command_create_mix(m):
    create_mix(m)


@bot.message_handler(commands=['in'])
def command_in_mix(m):
    in_mix(m)


@bot.message_handler(commands=['out'])
def command_out_mix(m):
    out_mix(m)


@bot.message_handler(commands=['list'])
def command_list_mix(m):
    list_mix(m)
	
@bot.message_handler(commands=['javigon'])
def command_javigon(m):
    get_javigon(m)
    
@bot.message_handler(commands=['zen'])
def command_zen(m):
    get_zen(m)


############################################
#                 POLLING                  #
############################################

bot.skip_pending = True
bot.polling()
