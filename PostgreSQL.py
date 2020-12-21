import psycopg2
from config import *
import os
bar.next() #7

def register(id, name):
    #INSERT INTO Transactions_By_TS.users (id, name, balance) VALUES (1, 'test', 25)
    global conn
    global cursor
    
    cursor.execute("INSERT INTO Transactions_by_ts.users (id, name) VALUES ('{id}', '{name}')".format(id=id, name=name))
    conn.commit()
bar.next() #8
    
def confirm(id, balance):
    #UPDATE transactions_by_ts.users SET balance = 0 WHERE id = 0
    global conn
    global cursor
    
    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(id=id, balance=balance))
    conn.commit()
bar.next() #9

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
bar.next() #21
 
def balance(id, question=False):
    #SELECT balance FROM transactions_by_ts.users WHERE id = 0
    global conn
    global cursor
    
    cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=id))
    record = cursor.fetchone()
    
    if question == True:
        if record == None:
            print(record == None, 'balance postgresql')
            return True
    
    return record
bar.next() #22

def create_order_BD(from_order, to_order, amount):
    #INSERT INTO transactions_by_ts.orders (from_order, to_order, amount) VALUES (1, 2, 3)
    global conn
    global cursor
    
    cursor.execute("INSERT INTO transactions_by_ts.orders (from_order, to_order, amount) VALUES ('{from_order}', '{to_order}', '{amount}')".format(from_order=from_order, to_order=to_order, amount=amount))
    
    cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=from_order))
    record = cursor.fetchone()
    
    cursor.execute("SELECT balance FROM transactions_by_ts.users WHERE id = '{id}'".format(id=to_order))
    record_to = cursor.fetchone()
    
    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(balance=record[0] - amount, id=from_order))
    
    cursor.execute("UPDATE transactions_by_ts.users SET balance = '{balance}' WHERE id = '{id}'".format(balance=record_to[0] + amount, id=to_order))
    
    conn.commit()
    