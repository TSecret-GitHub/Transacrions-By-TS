import telebot
from colorama import init, Fore
from telebot import types
from Keyboards import menu, confirm, yesNo, yesNo_for_order1, admin_keyboard
import PostgreSQL
from config import superadmin, is_superadmin, FORMATTER, LOG_FILE, FORMATTER_FILE, get_console_handler, get_file_handler, get_logger
from waiting_for_name import continue_text, callback_handler_step2, check_balance, create_order_step1, create_order_step2, create_order_step3, scp_5000
import time
from os import environ

console = input('~/> ')
while console != 'exit':
    if console[:7] == 'balance':
        ID = console[8:]
        
        print(PostgreSQL.balance(int(ID))[0])
    
    elif console[:8] == 'show all':
        records = PostgreSQL.program_participants()
        
        i = 0
        while i < len(records):
            print('----------' + records[i][1] + '----------')
            print('ID: ' + str(records[i][0]) + '\nБаланс: ' + str(records[i][2]) + '\nUsername: @' + str(records[i][4]))
            print('--------------------')
            
            i += 1
    
    elif console[:6] == 'add to':
        ID = console[7:]
        amount = int(input('add/> '))
        
        try:
            PostgreSQL.add_logics(ID, amount)
        except Exception as e:
            print(e)
    
    elif console[:6] == 'min to':
        ID = console[7:]
        amount = int(input('add/> '))
            
        try:
            PostgreSQL.minus_logics(ID, amount)
        except Exception as e:
            print(e)
    
    console = input('~/> ')
        