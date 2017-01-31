# -*- coding: utf-8 -*-
from collections import OrderedDict
import telebot
from telebot import types
import time
import sys
import random
from imp import reload

 
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
    mensaje = """🎮 *CS:GO FC NOOBS* [🎮](https://s27.postimg.org/xe8cfbzz7/CSGO_FC.png)

    Buenas compañeros, para un correcto funcionamiento del grupo y organización hemos creado un canal en discord con salas para que podamos comunicarnos por ahí cuando juguemos. Existen 4 salas, una *General* para todos los miembros que vayan entrando y después 3 salas para jugar (*Manqueando 1, 2, 3*).

    Cualquier mejora que propongais para facilitar la comunicación en Discord o Telegram podéis decirlo. 

    Enlace [Discord](https://discord.gg/C4xDC8n)
    """
    bot.send_message( cid, mensaje, parse_mode='Markdown')
    print ("Enviando info...")

 
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
            print (mensaje)
        elif m.content_type == 'new_chat_participant':
            bot.send_message( cid, 'Bienvenido '+ str(m.chat.first_name))
            command_info(m)
        

bot.set_update_listener(listener)
 
 
############################################
#                 COMANDOS                 #
############################################
 
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
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