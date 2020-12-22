import psycopg2
from config import *
from colorama import *
init(autoreset=True)

print(Fore.GREEN + 'Импорт модулей (PostgreSQL.py): Успех')

def register(id, name):
    #INSERT INTO Transactions_By_TS.users (id, name, balance) VALUES (1, 'test', 25)
    global conn
    global cursor

    cursor.execute("INSERT INTO Transactions_by_ts.users (id, name) VALUES ('{id}', '{name}')".format(id=id, name=name))
    conn.commit()
print(Fore.GREEN + 'Функция register() создана (PostgreSQL.py): Успех')

def confirm(id, balance):
    #UPDATE transactions_by_ts.users SET balance = 0 WHERE id = 0
    global conn
    global cursor

    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(id=id, balance=balance))
    conn.commit()
print(Fore.GREEN + 'Функция confirm() создана (PostgreSQL.py): Успех')

def block(id, question):
    global conn
    global cursor

    if question == True:
        cursor.execute("SELECT * FROM transactions_by_ts.users WHERE id = '{id}'".format(id=id))
        record = cursor.fetchone()

        try:
            if record[3] == True:
                return True
        except TypeError:
            return
    else:
        cursor.execute("UPDATE transactions_by_ts.users SET blocked = true WHERE id = '{id}'".format(id=id))
        conn.commit()
print(Fore.GREEN + 'Функция block() создана (PostgreSQL.py): Успех')

def balance(id, question=False):
    #SELECT balance FROM transactions_by_ts.users WHERE id = 0
    global conn
    global cursor

    cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=id))
    record = cursor.fetchone()

    if question == True:
        if record == None:
            return True

    return record
print(Fore.GREEN + 'Функция balance() создана (PostgreSQL.py): Успех')

def create_order_BD(from_order, to_order, amount):
    #INSERT INTO transactions_by_ts.orders (from_order, to_order, amount) VALUES (1, 2, 3)
    global conn
    global cursor

    #print(from_order, '- from_order')
    #print(to_order, '- to_order')
    #print(amount, '- amount')

    cursor.execute("INSERT INTO transactions_by_ts.orders (from_order, to_order, amount) VALUES ('{from_order}', '{to_order}', '{amount}')".format(from_order=from_order, to_order=to_order, amount=amount))

    debug_var = cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=from_order))
    record = cursor.fetchone()
    if record == None:
        print(Fore.RED + 'Ошибка: невозможно выполнить транзакцию, отправителя НЕ существует')
        print(Fore.MAGENTA + 'DEBUG: \nrecord:' + record + '\ncursor:' + debug_var)
        raise Exception('Вы не подтверждены!')

    cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=to_order))
    record_to = cursor.fetchone()
    if record_to == None:
        print(Fore.RED + 'Ошибка: невозможно выполнить транзакцию, получателя НЕ существует')
        raise Exception('Невозможно выполнить транзакцию, получателя *НЕ* существует')
        return

    if not record[0]:
        print(Fore.RED + 'Ошибка: баланс получателя отрицателен')
        print(Fore.MAGENTA + 'DEBUG: \nrecord_to:' + str(record[0]))
        raise Exception('Ваш баланс орицателен `=(`')
        return

    if not record[0] - amount:
        print(Fore.RED + 'Ошибка: На балансе недостаточно Логиков')
        raise Exception('На вашем балансе недостаточно логиков `=(`)')
        return

    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(balance=record[0] - amount, id=from_order))

    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(balance=record_to[0] + amount, id=to_order))

    conn.commit()
print(Fore.GREEN + 'Функция create_order_BD() создана (PostgreSQL.py): Успех')
