import sys
from importlib import reload

import telebot

############################################
#                 DATOS                    #
############################################
reload(sys)

TOKEN = '309560265:AAHBh78UeZkJPwUudgnC0KIunq3lp8Z8XZI'

bot = telebot.TeleBot(TOKEN)


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


def test(message):
    print("TEST")


############################################
#                 LISTENER                 #
############################################

def listener(messages):
    for message in messages:
        cid = message.chat.id
        file = open('message.txt', 'a')
        file.write(message + "\n")
        file.close()
        if message.content_type == 'text':
            if cid > 0:
                mensaje = str(message.chat.first_name) + " [" + str(cid) + "]: " + message.text
            else:
                mensaje = str(message.from_user.first_name) + "[" + str(cid) + "]: " + message.text
            f = open('log.txt', 'a')
            f.write(mensaje + "\n")
            f.close()
        elif message.content_type == 'new_chat_members':
            alias = " (@" + message.from_user.username + "). " if message.from_user.username is not None else ". "
            welcome = 'Bienvenido *' + str(message.from_user.first_name) + "*" + str(alias)
            info = "Aqui tienes toda la información..."
            if bot.get_chat(message.chat.id).pinned_message.text[:17] == '🎮 CS:GO FC NOOBS':
                bot.reply_to(bot.get_chat(message.chat.id).pinned_message, welcome + info, parse_mode='Markdown')
            else:
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


############################################
#                 POLLING                  #
############################################

bot.skip_pending = True
bot.polling(none_stop=True)
