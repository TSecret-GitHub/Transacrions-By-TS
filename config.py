import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import random
import string
import psycopg2
from colorama import init, Fore
import os
init(autoreset=True)


dbname = os.environ.get('dbname')
user = os.environ.get('user')
password = os.environ.get('password')
os.environ['SECRET_TOKEN'] = os.environ.get('SECRET_TOKEN')
os.environ['name'] = 'None'
os.environ['username'] = 'None'
superadmin = [799637030]
os.environ['command_to_update'] = '/bdbf0802da04452c385dba8d8cc405976ecb426a55546a11a13226c479e19872f6ce2a3e026b8003fcba508e11c30c0bfa3a9a1fd8e6672fc30de5af10929240'
os.environ['random_data'] = ''
os.environ['id'] = '0'
os.environ['amount'] = '0'
os.environ['status'] = 'None'
os.environ['addr'] = '0'
os.environ['SMH'] = 'False' #Separate Message Handler, for admins
os.environ['SMH help'] = '0'
os.environ['SMH id'] = '0'
os.environ['SMH amount'] = '0'
conn = psycopg2.connect(dbname=dbname, user=user,
                        password=password, host='localhost') #Здесь данные для БД
cursor = conn.cursor()
i = 0
FORMATTER = logging.Formatter(Fore.BLUE + "%(asctime)s, %(module)s.py:%(lineno)d | %(levelname)s — %(message)s")
LOG_FILE = "program.log"
FORMATTER_FILE = logging.Formatter("%(asctime)s, %(module)s.py:%(lineno)d. %(levelname)s — %(message)s \nLogger name: %(name)s\n")

print(Fore.GREEN + 'Создание переменных (config.py): Успех')

while i != 32:
    os.environ['random_data'] += random.choice(string.ascii_letters)
    i+=1

os.environ['command_to_update'] = '/service.' + os.environ.get('random_data')
print(Fore.GREEN + 'SUCCESS CREATED COMMAND (config.py): /' + os.environ.get('command_to_update'))

def is_superadmin(chat_id):
    if chat_id in superadmin:
        return True

    return False
#Вместо str(message.chat.id) == environ.get('superadmin')
#Теперь is_superadmin(message.chat.id)

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER_FILE)
    return file_handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) # лучше иметь больше логов, чем их нехватку
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
