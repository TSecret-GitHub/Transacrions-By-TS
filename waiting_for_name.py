#Импорт всех нужных файлов
import telebot
import sys
from config import superadmin
from Keyboards import menu, yesNo, yesNo_for_order, confirm
import PostgreSQL
from os import environ
from colorama import init, Fore
init(autoreset=True)

print(Fore.GREEN + 'Импорт модулей (waiting_for_name.py): Успех')

sys.setrecursionlimit(1000000)

# |-------continue_text-------|
# | Функция для регистрации
# | Вызывается для получения имени
# |-------continue_text-------|
def continue_text(message, bot):
    global confirm_message

    environ['name'] = message.text
    environ['username'] = str(message.from_user.username)

    if PostgreSQL.block(int(environ.get('addr')), True) is True:
        bot.send_message(int(environ.get('addr')), 'Вы *заблокированы*!', parse_mode='Markdown')
        return

    #print(type(addr))
    PostgreSQL.register(int(message.chat.id), environ.get('name'), environ.get('username'))
    bot.send_message(int(message.chat.id), 'Думаю все... \nОжидай когда тебя подтвердят...', reply_markup=menu)
    bot.send_message(superadmin[0], 'Подтвердить пользователя: \nОтправлено: @' + environ.get('username'), reply_markup=confirm)
    environ['status'] = 'None'
print(Fore.GREEN + 'Создание continue_text() (waiting_for_name.py): Успех')

def callback_handler_step2(message, bot):
    balance = message.text
    #print(message.text)

    #print(message.chat.id, '- message.chat.id')
    #print(environ.get('status'), '- status')

    #if message.chat.id != superadmin and status != 'waiting for balance.step1':
    #    print('canceled')
    #    return
    #if balance == True:
    #    bot.send_message(superadmin, '*Нет*, это должно быть целым числом`...`')
    #    status = 'waiting for balance'
    #    print('Zero')
    #    return


    #print(environ.get('addr'))
    #print(balance)
    try:
        int(balance)
    except ValueError:
        print(Fore.RED + 'Ошибка: баланс не целое число, повтор...')
        raise Exception('Это должно быть *целым* числом!')
    PostgreSQL.confirm(int(environ.get('addr')), message.text)
    #print('confirm OK')
    bot.send_message(int(environ.get('addr')), 'Вы были подтверждены!')
    #print('send_message OK')
    environ['status'] = 'None'
print(Fore.GREEN + 'Создание callback_handler_step2() (waiting_for_name.py): Успех')

def check_balance(message, bot):
    #if message.text.lower() == 'баланс':
    balance = PostgreSQL.balance(message.chat.id)
    PostgreSQL.balance(message.chat.id, True)

    if PostgreSQL.balance(message.chat.id, True) is True:
        bot.send_message(message.chat.id, 'Вы не подтверждены!')
        return

    bot.send_message(message.chat.id, 'Количество _Логиков_ на вашем аккаунте: ' + str(balance[0]), parse_mode='Markdown')
print(Fore.GREEN + 'Создание check_balance() (waiting_for_name.py): Успех')

def create_order_step1(message, bot):
    bot.send_message(message.chat.id, 'Введите username(Без "@") адресата ...')

    environ['status'] = 'waiting for id'
print(Fore.GREEN + 'Создание create_order_step1() (waiting_for_name.py): Успех')

def create_order_step2(message, bot):
    try:
        environ['id'] = str(PostgreSQL.ID_from_username(message.text))
    except Exception as e:
        bot.send_message(message.chat.id, e, parse_mode='Markdown')

    bot.send_message(message.chat.id, 'Введите количество логиков ...')
    environ['status'] = 'waiting for id.step2'
print(Fore.GREEN + 'Создание create_order_step2() (waiting_for_name.py): Успех')

def create_order_step3(message, bot):
    environ['amount'] = message.text

    try:
        int(environ.get('amount'))
    except:
        print(Fore.RED + 'Ошибка: amount состоит не только из цифр')
        raise Exception('Ну, а так-то здесь *должны* быть цифры')

    bot.send_message(message.chat.id, 'Все верно?: \nОтправить на (Подставлено на основе username): ' + environ.get('id') + '\nКоличество: ' + environ.get('amount'), reply_markup=yesNo_for_order)
    environ['status'] = 'None'
    #print(environ.get('status'))
print(Fore.GREEN + 'Создание create_order_step3() (waiting_for_name.py): Успех')
