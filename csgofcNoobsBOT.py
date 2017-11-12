# -*- coding: utf-8 -*-
import sys
from imp import reload

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


def command_info(m):
    cid = m.chat.id
    infile = open('util/info.txt', 'r', encoding='utf-8')
    mensaje = infile.read()
    infile.close()
    bot.send_message(cid, str(mensaje), parse_mode='Markdown')


############################################
#                 LISTENER                 #
############################################

def listener(messages):
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text':
            if cid > 0:
                mensaje = str(m.chat.first_name) + " [" + str(cid) + "]: " + m.text
            else:
                mensaje = str(m.from_user.first_name) + "[" + str(cid) + "]: " + m.text
            f = open('log.txt', 'a')
            f.write(mensaje + "\n")
            f.close()
        elif m.content_type == 'new_chat_participant':
            bot.send_message(cid, 'Bienvenido ' + str(m.chat.first_name))
            command_info(m)


bot.set_update_listener(listener)


############################################
#                 COMANDOS                 #
############################################

@bot.message_handler(commands=['start'])
def command_start(m):
    comando = m.text[7:]
    if comando == 'info':
        command_info(m)


@bot.message_handler(commands=['info'])
def command_z1(m):
    command_info(m)


############################################
#                 POLLING                  #
############################################

bot.skip_pending = True
bot.polling(none_stop=True)
