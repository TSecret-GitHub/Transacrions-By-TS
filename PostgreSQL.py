import psycopg2
from config import cursor, conn
from colorama import init, Fore
init(autoreset=True)

print(Fore.GREEN + 'Импорт модулей (PostgreSQL.py): Успех')

def register(id, name, username):
    #INSERT INTO Transactions_By_TS.users (id, name, balance) VALUES (1, 'test', 25)

    cursor.execute("INSERT INTO Transactions_by_ts.users (id, name, username) VALUES ('{id}', '{name}', '{username}')".format(id=id, name=name, username=username))
    conn.commit()
print(Fore.GREEN + 'Функция register() создана (PostgreSQL.py): Успех')

def confirm(id, balance):
    #UPDATE transactions_by_ts.users SET balance = 0 WHERE id = 0

    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(id=id, balance=balance))
    conn.commit()
print(Fore.GREEN + 'Функция confirm() создана (PostgreSQL.py): Успех')

def block(id, question):

    if question is True:
        cursor.execute("SELECT * FROM transactions_by_ts.users WHERE id = '{id}'".format(id=id))
        record = cursor.fetchone()

        try:
            if record[3] is True:
                return True
        except TypeError:
            return
    else:
        cursor.execute("UPDATE transactions_by_ts.users SET blocked = true WHERE id = '{id}'".format(id=id))
        conn.commit()
print(Fore.GREEN + 'Функция block() создана (PostgreSQL.py): Успех')

def balance(id, question=False):
    #SELECT balance FROM transactions_by_ts.users WHERE id = 0

    cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=id))
    record = cursor.fetchone()

    if question is True:
        if record is None:
            return True

    return record
print(Fore.GREEN + 'Функция balance() создана (PostgreSQL.py): Успех')

def create_order_BD(from_order, to_order, amount):
    #INSERT INTO transactions_by_ts.orders (from_order, to_order, amount) VALUES (1, 2, 3)

    #print(from_order, '- from_order')
    #print(to_order, '- to_order')
    #print(amount, '- amount')

    cursor.execute("INSERT INTO transactions_by_ts.orders (from_order, to_order, amount) VALUES ('{from_order}', '{to_order}', '{amount}')".format(from_order=from_order, to_order=to_order, amount=amount))

    debug_var = cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=from_order))
    record = cursor.fetchone()
    if record is None:
        print(Fore.RED + 'Ошибка: невозможно выполнить транзакцию, отправителя НЕ существует')
        print(Fore.MAGENTA + 'DEBUG: \nrecord:' + record + '\ncursor:' + debug_var)
        raise Exception('Вы не подтверждены!')

    debug_var = cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=to_order))
    record_to = cursor.fetchone()
    if record_to is None:
        print(Fore.RED + 'Ошибка: невозможно выполнить транзакцию, получателя НЕ существует')
        print(Fore.MAGENTA + 'DEBUG: \nrecord_to:' + record_to + '\ncursor:' + debug_var)
        raise Exception('Невозможно выполнить транзакцию, получателя *НЕ* существует')
        return

    print(Fore.MAGENTA + str(record) + '- record')
    if record[0] is True:
        print(Fore.RED + 'Ошибка: баланс получателя отрицателен')
        print(Fore.MAGENTA + 'DEBUG: \nrecord_to:' + str(record[0]))
        raise Exception('Ваш баланс орицателен `=(`)')
        return

    if record[0] - amount is True:
        print(Fore.RED + 'Ошибка: На балансе недостаточно Логиков')
        print(Fore.MAGENTA + 'DEBUG: \nrecord_to:' + str(record[0]))
        raise Exception('На вашем балансе недостаточно логиков `=(`')
        return

    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(balance=record[0] - amount, id=from_order))

    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(balance=record_to[0] + amount, id=to_order))

    conn.commit()
print(Fore.GREEN + 'Функция create_order_BD() создана (PostgreSQL.py): Успех')

def add_logics(id, amount):
    cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=id))
    record = cursor.fetchone()

    if record is None:
        print(Fore.RED + 'Ошибка: Записи не существует')
        raise Exception('ID *не* существует!')

    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(balance=record[0]+int(amount), id=id))

    conn.commit()

def ID_from_username(username):
    cursor.execute("SELECT id FROM transactions_by_ts.users WHERE username = '{username}'".format(username=username))
    record = cursor.fetchone()

    if record is None:
        print(Fore.RED + 'Ошибка: Записи не существует!')
        raise Exception('Такого username нет в Базе Данных')
        return

    return record[0]

def minus_logiks(id, amount):
    cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=id))
    record = cursor.fetchone()

    if record is None:
        print(Fore.RED + 'Ошибка: Записи не существует')
        raise Exception('Такого username нет в Базе Данных')
        return

    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(balance=record[0]-amount, id=id))
    conn.commit()

def program_participants():
    cursor.execute("SELECT * FROM transactions_by_ts.users")
    records = cursor.fetchall()

    i = 0
    while i < len(records):
        print('-------------------------')
        print(records[i][1] + ':', '\nID:',  records[i][0], '\nБаланс:', records[i][2], '\nUsername: @' + records[i][4])
        print('-------------------------')
        i += 1
    return records

program_participants()
