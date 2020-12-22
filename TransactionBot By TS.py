#importing modules, and for telegram...
#from config import *
import telebot
from colorama import init, Fore
from telebot import types
from Keyboards import menu, confirm, yesNo, yesNo_for_order1, admin_keyboard
import PostgreSQL
from waiting_for_name import continue_text, callback_handler_step2, check_balance, create_order_step1, create_order_step2, create_order_step3
import time
from os import environ
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
    environ['status'] = 'None'

    bot.send_message(message.chat.id, 'Привет, начнем! \nЗарегистрируйся ==>')
    bot.send_message(message.chat.id, 'Напиши имя')

    environ['status'] = 'waiting for name'
#-Хендлер для команды /start
print(Fore.GREEN + 'Директива для команды /start (Основной файл): Успех')

#Хендлер для команды //service.command_to_update
@bot.message_handler(commands=[command_to_update])
def update_superadmin_chat_id(message):
    environ['status'] = 'None'

    print(Fore.MAGENTA + 'DEBUG: Заход в блок service.command_to_update')
    print(Fore.MAGENTA + 'DEBUG: Chat ID: ' + str(message.chat.id))
    print(Fore.MAGENTA + 'DEBUG: Username: ' + message.from_user.username)

    environ['superadmin'] = str(message.chat.id)
    print(Fore.MAGENTA + 'DEBUG: Superadmin переназначен: ' + environ.get('superadmin'))

    bot.send_message(message.chat.id, 'Обновлено!')

#@bot.message_handler(commands=['get_admin.on', 'get_admin.off'])
#def get_admin(message):
#    if str(message.chat.id) == environ.get('superadmin') and message.text == '/get_admin.on':
#        environ['SMH'] = 'True'
#        bot.send_message(message)
#    else:
#        print(Fore.YELLOW + 'WARNING: отклонён запрос get_admin.on, подробности: @' + str(message.from_user.username))
#        bot.send_message(message.chat.id, 'Забавно что ты сюда попал :) \nНо, я тебя не дам использовать эту команду, она не для тебя... \nПросто забудь об этом. \nИтак, Я збрасываю функцию \nВсе еще странно то, что ты смог дойти хоть сюда =)', parse_mode='Markdown')
#        return

#Хендлер для команды //service.command_to_update
print(Fore.GREEN + 'Директива для команды //service.command_to_update (Основной файл): Успех')

#Основной хендлер который направляет сообщения по функциям
@bot.message_handler(content_types=['text'])
def content_types_text(message):
    if environ.get('status') == 'waiting for name':
        print(Fore.LIGHTMAGENTA_EX + 'INFO: Начата регистрация')
        environ['addr'] = str(message.chat.id)
        continue_text(message, bot)
        return
    elif str(message.chat.id) == environ.get('superadmin') and environ.get('status') == 'waiting for balance.step1':
        try:
            callback_handler_step2(message, bot)
        except Exception as e:
            bot.send_message(message.chat.id, e, parse_mode='Markdown')

        return
    elif message.text.lower() == 'баланс':
        environ['addr'] = str(message.chat.id)
        check_balance(message, bot)
        return

    elif message.text.lower() == 'статус':
        print(Fore.MAGENTA + 'DEBUG: status')
        bot.send_message(message.chat.id, 'Твой ID: ' + str(message.chat.id))

    #-------------------------------------------------------------------
    if message.text.lower() == 'перевести':
        environ['addr'] = str(message.chat.id)
        environ['help var'] = str(message.chat.id)

        create_order_step1(message, bot)
        print(Fore.MAGENTA + environ.get("help var"))
        print(Fore.MAGENTA + environ.get("addr"))
        print(Fore.MAGENTA + environ.get("status"))

        return
    if environ.get('status') == 'waiting for id' and environ.get("help var") == str(message.chat.id):
        print(Fore.MAGENTA + 'TEST')
        environ['addr'] = str(message.chat.id)
        try:
            create_order_step2(message, bot)
        except Exception as e:
            bot.send_message(message.chat.id, e, parse_mode='Markdown')
        return
    if environ.get('status') == 'waiting for id.step2' and environ.get("help var") == str(message.chat.id):
        environ['addr'] = str(message.chat.id)
        try:
            create_order_step3(message, bot)
        except Exception as e:
            bot.send_message(message.chat.id, e, parse_mode='Markdown')
        return
    #-------------------------------------------------------------------


print(Fore.GREEN + 'Директива для сообщений (Основной файл): Успех')

#Хендлер на Callback`и
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "confirm":
        environ['status'] = 'waiting for balance.step1'
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
        if PostgreSQL.balance(int(environ.get('addr')), True) is True:
            bot.send_message(int(environ.get('addr')), 'Вы не подтверждены!')
            return

        #print(environ.get('amount'), '- amount')
        try:
            PostgreSQL.create_order_BD(int(environ.get('addr')), int(environ.get('id')), int(environ.get('amount')))
        except Exception as e:
            bot.send_message(int(environ.get('addr')), e, parse_mode='Markdown')
            return
        bot.send_message(int(environ.get('addr')), 'Готово! \nOrder создан')
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
