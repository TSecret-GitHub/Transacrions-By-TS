#Импорт всех нужных файлов
import telebot
import sys
from config import *
from Keyboards import *
import PostgreSQL
from os import *

sys.setrecursionlimit(1000000)
bar.next() #10

# |-------continue_text-------|
# | Функция для регистрации
# | Вызывается для получения имени
# |-------continue_text-------|
def continue_text(message, bot):
    global menu
    global confirm
    environ['name'] = message.text
    environ['username'] = str(message.from_user.username)

    if PostgreSQL.block(int(environ.get('addr')), True) == True:
        bot.send_message(int(environ.get('addr')), 'Вы *заблокированы*!', parse_mode='Markdown')
        return

    print(environ.get('addr'), '- addr')
    #print(type(addr))
    PostgreSQL.register(int(message.chat.id), environ.get('name'))
    bot.send_message(int(message.chat.id), 'Думаю все... \nОжидай когда тебя подтвердят...', reply_markup=menu)
    bot.send_message(int(environ.get('superadmin')), 'Подтвердить пользователя: \nОтправлено: @' + environ.get('username'), reply_markup=confirm)
    environ['status'] = 'None'
bar.next() #11

def callback_handler_step2(message, bot):
    print('step 2')

    global is_number
    balance = is_number(message.text)
    print(message.text)

    print(message.chat.id, '- message.chat.id')
    print(environ.get('status'), '- status')

    #if message.chat.id != superadmin and status != 'waiting for balance.step1':
    #    print('canceled')
    #    return
    #if balance == True:
    #    bot.send_message(superadmin, '*Нет*, это должно быть целым числом`...`')
    #    status = 'waiting for balance'
    #    print('Zero')
    #    return

    print(environ.get('addr'))
    print(balance)
    PostgreSQL.confirm(int(environ.get('addr')), message.text)
    print('confirm OK')
    bot.send_message(int(environ.get('addr')), 'Вы были подтверждены!')
    print('send_message OK')
bar.next() #12

def check_balance(message, bot):
    #if message.text.lower() == 'баланс':
    balance = PostgreSQL.balance(message.chat.id)
    test_balance = PostgreSQL.balance(message.chat.id, True)

    if PostgreSQL.balance(message.chat.id, True) == True:
        bot.send_message(message.chat.id, 'Вы не подтверждены!')
        return

    bot.send_message(message.chat.id, 'Количество _Логиков_ на вашем аккаунте: ' + str(balance[0]), parse_mode='Markdown')
bar.next() #24

def create_order_step1(message, bot):
    bot.send_message(message.chat.id, 'Введите id адресата ...')
    environ['status'] = 'waiting for id'
bar.next() #25

def create_order_step2(message, bot):
    environ['id'] = message.text

    bot.send_message(message.chat.id, 'Введите количество логиков ...')
    environ['status'] = 'waiting for id.step2'
bar.next() #26

def create_order_step3(message, bot):
    global yesNo_for_order
    environ['amount'] = message.text

    bot.send_message(message.chat.id, 'Все верно?: \nОтправить на: ' + environ.get('id') + '\nКоличество: ' + environ.get('amount'), reply_markup=yesNo_for_order)
    environ['status'] = 'None'
    print(environ.get('status'))
bar.next() #27
