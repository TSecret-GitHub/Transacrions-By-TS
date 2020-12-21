#importing modules, and for telegram...
from config import *
import telebot
from colorama import *
from telebot import types
from Keyboards import *
import PostgreSQL
from waiting_for_name import *
import time
from os import *
init(autoreset=True)
#-Импорты
print(Fore.GREEN + 'Импорт модулей (Основной файл): Успех')

#Переменные
init(autoreset=True)
#telebot.logger.setLevel(__import__('logging').DEBUG)
bot = telebot.TeleBot(environ.get('SECRET_TOKEN'))
command_to_update = environ.get('command_to_update')
#-Переменные
print(Fore.GREEN + 'Создание переменных (Основной файл): Успех')

#Хендлер для команды /start
@bot.message_handler(commands=['start'])
def start_message(message):

    bot.send_message(message.chat.id, 'Привет, начнем! \nЗарегистрируйся ==>')
    bot.send_message(message.chat.id, 'Напиши имя')

    environ['addr'] = str(message.chat.id)
    environ['status'] = 'waiting for name'
#-Хендлер для команды /start
print(Fore.GREEN + 'Директива для команды /start (Основной файл): Успех')

#Хендлер для команды //service.command_to_update
@bot.message_handler(commands=[command_to_update])
def update_superadmin_chat_id(message):
    print('test block command_to_update')
    environ['superadmin'] = str(message.chat.id)
    print(environ.get('superadmin'))
    bot.send_message(message.chat.id, 'Обновлено!')
#Хендлер для команды //service.command_to_update
print(Fore.GREEN + 'Директива для команды //service.command_to_update (Основной файл): Успех')

#Основной хендлер который направляет сообщения по функциям
@bot.message_handler(content_types=['text'])
def content_types_text(message):
    environ['addr'] = str(message.chat.id)

    if environ.get('status') == 'waiting for name':
        continue_text(message, bot)
        return
    print(type(environ.get('superadmin')))
    print(type(message.chat.id))
    if str(message.chat.id) == environ.get('superadmin') and environ.get('status') == 'waiting for balance.step1':
        print('if ok')
        callback_handler_step2(message, bot)
        return
    if message.text.lower() == 'баланс':
        check_balance(message, bot)
        return
    if message.text.lower() == 'перевести':
        create_order_step1(message, bot)
        return
    if environ.get('status') == 'waiting for id':
        print('waiting for id')
        try:
            create_order_step2(message, bot)
        except Exception as e:
            bot.send_message(message.chat.id, e, parse_mode='Markdown')
        return
    if environ.get('status') == 'waiting for id.step2':
        try:
            create_order_step3(message, bot)
        except Exception as e:
            bot.send_message(message.chat.id, e, parse_mode='Markdown')
        return
print(Fore.GREEN + 'Директива для сообщений (Основной файл): Успех')

#Хендлер на Callback`и
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print('step callback 2')
    if call.data == "confirm":
        environ['status'] = 'waiting for balance.step1'
        print('step callback 3')
        print('status -', environ.get('status'))
        bot.send_message(int(environ.get('superadmin')), 'Balance')

    elif call.data == 'cancel':
        bot.send_message(int(environ.get('addr')), 'Вас отклонили, повторить?', reply_markup=yesNo)

    elif call.data == 'yes':
        bot.send_message(int(environ.get('addr')), 'Отправлено...', reply_markup=menu)
        bot.send_message(int(environ.get('superadmin')), 'Подтвердить пользователя: \nОтправлено: @' + environ.get('username') + '\nПовторная отправка...', reply_markup=confirm)

    elif call.data == 'no':
        bot.edit_message_text(chat_id=int(environ.get('addr')), message_id=call.message.message_id, text="Ну и ладно...")
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Ну и ладно...")

    elif call.data == 'block':
        PostgreSQL.block(int(environ.get('addr')), False)
        bot.send_message(int(environ.get('addr')), 'Вас *заблокировали*!', parse_mode='Markdown')

    elif call.data == 'yes.order':
        if PostgreSQL.balance(int(environ.get('addr')), True) == True:
            bot.send_message(int(environ.get('addr')), 'Вы не подтверждены!')
            return

        print(environ.get('amount'), '- amount')
        try:
            PostgreSQL.create_order_BD(int(environ.get('addr')), int(environ.get('id')), int(environ.get('amount')))
        except Exception as e:
            bot.send_message(int(environ.get('addr')), e, parse_mode='Markdown')
            return
        bot.send_message(int(environ.get('addr')), 'Готово! \nOrder создан, подробнее - /orders')
    #elif call.data == 'yes.order':
    #    global id
    #    global amount

    #    print(id, '- id')
    #    print(amount, '- amount')

print(Fore.GREEN + 'Директива для Callback`ов (Основной файл): Успех')

print(Fore.GREEN + 'Загрузка завершена, запускаю bot.polling...')
time.sleep(1)
print('\n')
bot.polling(none_stop=True)
