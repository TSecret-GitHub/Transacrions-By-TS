#importing modules, and for telegram...
#from config import *
import telebot
from colorama import init, Fore
from telebot import types
from Keyboards import menu, confirm, yesNo, yesNo_for_order1, admin_keyboard
import PostgreSQL
from threading import Thread
from config import superadmin, is_superadmin, FORMATTER, LOG_FILE, FORMATTER_FILE, get_console_handler, get_file_handler, get_logger
from waiting_for_name import continue_text, callback_handler_step2, check_balance, create_order_step1, create_order_step2, create_order_step3, scp_5000
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
log = get_logger("__main__")
#-Переменные
print(Fore.GREEN + 'Создание переменных (Основной файл): Успех')

#Хендлер для команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    environ['status'] = 'None'
    environ['username'] = str(message.from_user.username)
    if message.from_user.username is None:
        bot.send_message(message.chat.id, 'Есть проблема! \nВаш username определен! Вам надо [назначить](https://bit.ly/3mNJzFi) имя пользователя!', parse_mode='Markdown')

    bot.send_message(message.chat.id, 'Привет, начнем! \nЗарегистрируйся ==>')
    bot.send_message(message.chat.id, 'Напиши имя')

    environ['status'] = 'waiting for name'
#-Хендлер для команды /start
print(Fore.GREEN + 'Директива для команды /start (Основной файл): Успех')

#Хендлер для команды /donate
@bot.message_handler(commands=['donate'])
def DONATE(message):
    bot.send_message(message.chat.id, 'Вау! Ты написал это! \nСпасибо, вот [ссылка](https://www.patreon.com/tsecret) на мой *Patreon*. \nЕсли на Spotify, то выбирай план за $5 \n`:D`', parse_mode='Markdown')
#-Хендлер для команды /start
print(Fore.GREEN + 'Директива для команды /start (Основной файл): Успех')

#Хендлер для команды //service.command_to_update
@bot.message_handler(commands=[command_to_update])
def update_superadmin_chat_id(message):
    log.warning(Fore.YELLOW + '//service.command_to_update started' + Fore.BLUE)

    environ['status'] = 'None'

    log.warning(Fore.YELLOW + 'DEBUG: Chat ID: ' + str(message.chat.id) + '\n   >DEBUG: Username: ' + message.from_user.username)

    superadmin.append(message.chat.id)
    log.info(Fore.GREEN + 'DEBUG: Superadmin переназначен: ' + str(superadmin))

    bot.send_message(message.chat.id, 'Обновлено!')

@bot.message_handler(commands=['get_admin.on', 'get_admin.off'])
def get_admin(message):
    log.debug(message.text)
    if  is_superadmin(message.chat.id) and message.text == '/get_admin.on':
        environ['SMH'] = 'True'
        bot.send_message(message.chat.id, 'Это инструкция, но её нет. Мне просто было лень её писать...')
        bot.send_message(message.chat.id, 'Отправляю клавиатуру...', reply_markup=admin_keyboard)

    elif is_superadmin(message.chat.id) and message.text == '/get_admin.off':
        log.debug('/get_admin.off')
        environ['SMH'] = 'True'
        bot.send_message(message.chat.id, 'Выход...', reply_markup=menu)

    else:
        log.warning(Fore.YELLOW + 'WARNING: отклонён запрос get_admin.on, подробности: \n   >@' + str(message.from_user.username))
        bot.send_message(message.chat.id, 'Забавно что ты сюда попал :) \nНо, я тебя не дам использовать эту команду, она не для тебя... \nПросто забудь об этом. \nИтак, Я збрасываю функцию \nВсе еще странно то, что ты смог дойти хоть сюда =)', parse_mode='Markdown')
        return

#Хендлер для команды //service.command_to_update
print(Fore.GREEN + 'Директива для команды //service.command_to_update (Основной файл): Успех')

#Основной хендлер который направляет сообщения по функциям
@bot.message_handler(content_types=['text'])
def content_types_text(message):
    if is_superadmin(message.chat.id) is False:
        log.debug(str(message.chat.id))
        environ['addr'] = str(message.chat.id)
    if PostgreSQL.block(int(environ.get('addr')), True) is True:
        bot.send_message(int(environ.get('addr')), 'Вы *заблокированы*!', parse_mode='Markdown')
        return

    if environ.get('SMH') == 'True':
        if message.text.lower() == 'добавить логики':
            environ['status'] = 'добавить логики'
            environ['SMH help'] = str(message.chat.id)

            bot.send_message(message.chat.id, 'Введите количество:')
        elif message.text.lower() == 'отнять логики':
            environ['status'] = 'отнять логики'
            environ['SMH help'] = str(message.chat.id)

            bot.send_message(message.chat.id, 'Введите количество:')

        elif environ.get('status') == 'отнять логики' and environ.get('SMH help') == str(message.chat.id):
            try:
                int(message.text)
            except ValueError:
                log.error(Fore.RED + 'Отнимание логиков: \n>Username: @' + message.from_user.username)
                bot.send_message(message.chat.id, 'Цифры!')
                return

            environ['status'] = 'отнять логики.1'
            environ['SMH amount'] = str(message.text)

            bot.send_message(message.chat.id, 'Введите username(Без знака "@") получателя:')

        elif environ.get('status') == 'отнять логики.1' and environ.get('SMH help') == str(message.chat.id):
            try:
                ID = PostgreSQL.ID_from_username(message.text)
            except Exception as e:
                log.error(Fore.RED + 'Отнимание логиков: \n   >Exception: ' + e)
                bot.send_message(message.chat.id, e, parse_mode='Markdown')

            try:
                PostgreSQL.minus_logiks(ID, int(environ.get('SMH amount')))
            except Exception as e:
                log.error(Fore.RED + 'Отнимание логиков: \n   >Exception: ' + e)
                bot.send_message(message.chat.id, e, parse_mode='Markdown')
            bot.send_message(message.chat.id, 'Готово!', parse_mode='Markdown')

            environ['status'] = 'None'
        elif message.text.lower() == 'заблокировать':
            environ['status'] = 'заблокировать'
            environ['SMH help'] = str(message.chat.id)

            bot.send_message(message.chat.id, 'Введите username(Без знака "@"):')

        elif environ.get('status') == 'заблокировать' and environ.get('SMH help') == str(message.chat.id):
            try:
                ID = PostgreSQL.ID_from_username(message.text)
            except Exception as e:
                log.error(Fore.RED + 'Заблокировать: \n   >Exception: ' + e)
                bot.send_message(message.chat.id, e, parse_mode='Markdown')

            PostgreSQL.block(ID)
            bot.send_message(message.chat.id, 'Готово!', parse_mode='Markdown')
            environ['status'] = 'None'

        elif message.text.lower() == 'участники этой программы':
            records = PostgreSQL.program_participants()

            i = 0
            while i < len(records):
                bot.send_message(message.chat.id, str(records[i][1]) + ':' + '\nID: ' + str(records[i][0]) + '\nБаланс: ' + str(records[i][2]) + '\nUsername: @' + str(records[i][4]))
                log.info(Fore.GREEN + str(records[i][1]))
                i += 1
        elif environ.get('status') == 'добавить логики' and environ.get('SMH help') == str(message.chat.id):
            try:
                int(message.text)
            except ValueError:
                log.error(Fore.RED + 'Добавить логики: \n   >Exception: ' + e)
                bot.send_message(message.chat.id, 'Цифры!')
                return

            environ['SMH amount'] = str(message.text)
            environ['status'] = 'добавить логики.1'

            bot.send_message(message.chat.id, 'Введите username(Без знака "@") получателя:')
        elif environ.get('status') == 'добавить логики.1' and environ.get('SMH help') == str(message.chat.id):
            try:
                ID = PostgreSQL.ID_from_username(message.text)
            except Exception as e:
                log.error(Fore.RED + 'Добавить логики: \n   >Exception: ' + e)
                bot.send_message(message.chat.id, e, parse_mode='Markdown')
            environ['SMH id'] = str(message.text)
            environ['status'] = 'добавить логики.2'

            try:
                PostgreSQL.add_logics(ID, environ.get('SMH amount'))
            except Exception as e:
                log.error(Fore.RED + 'Добавить логики: \n   >Exception: ' + e)
                bot.send_message(message.chat.id, e, parse_mode='Markdown')
            bot.send_message(message.chat.id, 'Готово!')

            environ['status'] = 'None'

    if environ.get('status') == 'waiting for name':
        log.info(Fore.LIGHTMAGENTA_EX + 'INFO: Начата регистрация')
        environ['addr'] = str(message.chat.id)
        continue_text(message, bot)
        return
    elif message.text == 'Почему?':
        log.info(Fore.GREEN + 'Пользователь @' + message.from_user.username + ' нашел ' + Fore.RED + 'ЭТО!')
        scp_5000(message, bot)
    elif is_superadmin(message.chat.id) and environ.get('status') == 'waiting for balance.step1':
        try:
            callback_handler_step2(message, bot)
        except Exception as e:
            log.error(Fore.RED + 'Добавить логики: \n   >Exception: ' + e)
            bot.send_message(message.chat.id, e, parse_mode='Markdown')

        return
    elif message.text.lower() == 'баланс':
        environ['addr'] = str(message.chat.id)
        check_balance(message, bot)
        return
    elif message.text.lower() == 'статус':
        log.debug(Fore.MAGENTA + 'status')
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
            log.error(Fore.RED + 'Waiting for id: \n   >Exception: ' + e)
            bot.send_message(message.chat.id, e, parse_mode='Markdown')
        return
    if environ.get('status') == 'waiting for id.step2' and environ.get("help var") == str(message.chat.id):
        environ['addr'] = str(message.chat.id)
        try:
            create_order_step3(message, bot)
        except Exception as e:
            log.error(Fore.RED + 'Waiting for id.step2: \n   >Exception: ' + e)
            bot.send_message(message.chat.id, e, parse_mode='Markdown')
        return
    #-------------------------------------------------------------------


print(Fore.GREEN + 'Директива для сообщений (Основной файл): Успех')

#Хендлер на Callback`и
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "confirm":
        environ['status'] = 'waiting for balance.step1'
        bot.send_message(superadmin[0], 'Balance')

    elif call.data == 'cancel':
        bot.send_message(int(environ.get('addr')), 'Вас отклонили, повторить?', reply_markup=yesNo)

    elif call.data == 'yes':
        bot.send_message(int(environ.get('addr')), 'Отправлено...', reply_markup=menu)
        bot.send_message(superadmin[0], 'Подтвердить пользователя: \nОтправлено: @' + environ.get('username') + '\nПовторная отправка...', reply_markup=confirm)

    elif call.data == 'no':
        bot.edit_message_text(chat_id=int(environ.get('addr')), message_id=call.message.message_id, text="Ну и ладно...")
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Ну и ладно...")

    elif call.data == 'block':
        PostgreSQL.block(int(environ.get('addr')), False)
        bot.send_message(int(environ.get('addr')), 'Вас *заблокировали*!', parse_mode='Markdown')

    elif call.data == 'yes.order':
        if PostgreSQL.balance(int(environ.get('addr')), True) is True:
            bot.send_message(int(environ.get('addr')), 'Вы не подтверждены!')
            return

        try:
            PostgreSQL.create_order_BD(int(environ.get('addr')), int(environ.get('id')), int(environ.get('amount')))
        except Exception as e:
            bot.send_message(int(environ.get('addr')), e, parse_mode='Markdown')
            return
        bot.send_message(int(environ.get('addr')), 'Готово! \nOrder создан')
    elif call.data == 'yes.scp':
        log.debug(environ.get('addr'))
        log.info(int(environ.get('addr')) + ' - call.data YES')
        bot.send_message(int(environ.get('addr')), '[Ссылка](http://scpfoundation.net/scp-5000)', parse_mode='Markdown')
        try:
            PostgreSQL.add_logics(int(environ.get('addr')), 3)
        except Exception as e:
            bot.send_message('Произошла проблема')
            log.error(Fore.RED + e + ' - дайте 3 логика и помогите зарегистрироваться')
            log.debug(Fore.MAGENTA + environ.get('addr'))
        bot.send_sticker(int(environ.get('addr')), 'CAACAgUAAxkBAAEBtpBf5K1P3AoxKFT5Yl2olmGEOOiBMwACJgEAAp3nwFTBaGgDdc8qxR4E')
        bot.send_message(int(environ.get('addr')), 'Вам подарено 3 логика, поздравляю')
    elif call.data == 'no.scp':
        log.info(int(environ.get('addr')) + ' - call.data NO')
        bot.edit_message_text(chat_id=int(environ.get('addr')), message_id=call.message.message_id, text="Хорошо...")
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Хорошо...")
        PostgreSQL.add_logics(int(environ.get('addr')), 3)
        bot.send_sticker(int(environ.get('addr')), 'CAACAgEAAxkBAAEBto5f5K1BIucGuvxcicQ_kAzUseL3PAACVTMAAtpxZgdUSKRTBteYgR4E')
        bot.send_message(int(environ.get('addr')), 'Вам подарено 3 логика, поздравляю')

print(Fore.GREEN + 'Директива для Callback`ов (Основной файл): Успех')

print(Fore.GREEN + 'Загрузка завершена, запускаю bot.polling...')
time.sleep(1)
print('\n')
try:
    bot.polling(none_stop=True)
except Exception as e:
    log.error(Fore.RED + str(e))
    log.info(Fore.GREEN + 'Переподключение...')

    bot.polling(none_stop=True)
