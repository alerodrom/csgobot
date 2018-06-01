import sys
import os
from importlib import reload
import telebot
from db_helper import DBHelper
from telebot import types
############################################
#                 DATOS                    #
############################################
reload(sys)


TOKEN = os.environ.get('csgo_bot_token')

bot = telebot.TeleBot(TOKEN)
# It avoids flooding with commands , True to activate(default False)
evitar_flood_javigon = True
db = DBHelper()
db.setup()

# test -1001280311618
# CSGO -1001107551770
# test jesus -319789223
GROUP_ID = -1001107551770

ADMINS = [
    6879883,
    15418061,
    150147251,
    258786599,
    1346477,
    264856075,
    39284761,
    2622857]

############################################
#                 DECORATORS               #
############################################


def custom_group_only(func):
    def func_wrapper(message):
        if message.chat.id != GROUP_ID:
            message_text = ("Este comando solo esta disponible para el grupo "
                            + "de CSGO:NOOBS")
            bot.send_message(message.chat.id, message_text)
            return
        func(message)
    return func_wrapper


def is_admin(func):
    def func_wrapper(message):
        if message.from_user.id not in ADMINS:
            bot.send_message(message.chat.id, "No eres admin.")
        func(message)
    return func_wrapper


############################################
#                 FUNCIONES                #
############################################


def get_info(message):
    chat_id = message.chat.id
    with open('util/info.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        bot.send_message(chat_id, str(text), parse_mode='Markdown')


def echo(message):
    chat_id = message.chat.id
    text = ("Hola " + message.from_user.first_name + " has puesto: "
            + message.text[6:])
    bot.send_message(chat_id, str(text), parse_mode='Markdown')


@custom_group_only
@is_admin
def create_mix(message):
    chat_id = message.chat.id
    msg = db.create_mix(str(message.text[12:]))
    bot.send_message(chat_id, msg)


@custom_group_only
def in_mix(message):
    chat_id = message.chat.id
    user = message.from_user
    alias = "@" + user.username if user.username else user.first_name
    db.add_item(str(user.id), str(user.first_name), alias)
    msg = 'Te has añadido correctamente ' + str(alias)
    bot.send_message(chat_id, msg)


@custom_group_only
def out_mix(message):
    chat_id = message.chat.id
    user = message.from_user
    alias = "@" + user.username if user.username else user.first_name
    db.delete_item(str(user.id))
    msg = 'Te has eliminado correctamente ' + str(alias)
    bot.send_message(chat_id, msg)


@custom_group_only
def list_mix(message):
    chat_id = message.chat.id
    items = db.get_items()
    bot.send_message(chat_id, items, parse_mode='Markdown')


@custom_group_only
def get_javigon(message):
    try:
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('/sinDuda')
        itembtn2 = types.KeyboardButton('/pollon')
        markup.add(itembtn1, itembtn2)
        bot.send_message(chat_id, "Elige tu audio:", reply_markup=markup)

    except BaseException:
        print("Oops!Try again...")


@custom_group_only
def get_sinDuda(message):
    chat_id = message.chat.id
    if evitar_flood_javigon:  # evita el flood
        try:
            # elimina los mensajes para evitar flood
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id)

        except(Exception, ArithmeticError) as e:

            bot.send_message(
                chat_id, "Oops! No soy ADMIN?,El antiflood requiere que sea admin.")

    try:
        markup = types.ReplyKeyboardRemove(
            selective=False)  # elimina teclado de pantalla
        bot.send_audio(
            chat_id=chat_id, audio=open(
                'javigon_sinDuda_audio.ogg', 'rb'))
        bot.send_message(
            chat_id,
            "ok reproduciendo sinDuda",
            reply_markup=markup)
    except(Exception, ArithmeticError) as e:
        print("Oops! Archivo javigon_sinDuda_audio.ogg not found.")
        bot.send_message(chat_id, "Audio no encontrado contacta con Admin")


@custom_group_only
def get_pollon(message):
    chat_id = message.chat.id
    if evitar_flood_javigon:  # evita el flood
        try:
            # elimina los mensajes para evitar flood
            bot.delete_message(message.chat.id, message.message_id - 1)

            bot.delete_message(message.chat.id, message.message_id)

        except(Exception, ArithmeticError) as e:

            bot.send_message(
                chat_id, "Oops! No soy ADMIN?,El antiflood requiere que sea admin.")

    try:
        markup = types.ReplyKeyboardRemove(
            selective=False)  # elimina teclado de pantalla

        bot.send_audio(
            chat_id=chat_id, audio=open(
                'javigon_pollon_audio.ogg', 'rb'))
        bot.send_message(
            chat_id,
            "ok reproduciendo pollon",
            reply_markup=markup)

    except(Exception, ArithmeticError) as e:
        print("Oops! Archivo javigon_pollon_audio.ogg not found.")
        bot.send_message(
            chat_id,
            "Audio no encontrado, contacta con Admin",
            reply_markup=markup)


############################################
#                 LISTENER                 #
############################################

def listener(messages):
    for message in messages:
        if message.content_type == 'text':
            cid = message.chat.id
            mensaje = (message.chat.first_name if cid > 0
                       else message.from_user.first_name)
            mensaje += "[" + str(cid) + "]: " + message.text
            with open('log.txt', 'a') as f:
                f.write(mensaje + "\n")
        elif message.content_type == 'new_chat_members':
            for user in message.new_chat_members:
                alias = (" (@" + user.username + "). " if user.username
                         else ". ")
                welcome = 'Bienvenido *' + user.first_name + "*" + alias
                bot.send_message(message.chat.id, welcome,
                                 parse_mode='Markdown')
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


@bot.message_handler(commands=['sinDuda'])
def command_sinDuda(m):
    get_sinDuda(m)


@bot.message_handler(commands=['pollon'])
def command_pollon(m):
    get_pollon(m)

############################################
#                 POLLING                  #
############################################


bot.skip_pending = True
bot.polling()
