import random
import string
import psycopg2
from colorama import *
import os
init(autoreset=True)
print(Fore.GREEN + 'Импорт модулей (config.py): Успех')

os.environ['SECRET_TOKEN'] = '1425645766:AAFrtZBrvQ0M95b7uFEv748WAUbTeaAXt-c'
os.environ['name'] = 'None'
os.environ['username'] = 'None'
os.environ['superadmin'] = '799637030'
os.environ['command_to_update'] = '/bdbf0802da04452c385dba8d8cc405976ecb426a55546a11a13226c479e19872f6ce2a3e026b8003fcba508e11c30c0bfa3a9a1fd8e6672fc30de5af10929240'
os.environ['random_data'] = ''
os.environ['id'] = '0'
os.environ['amount'] = '0'
os.environ['status'] = 'None'
os.environ['addr'] = '0'
conn = psycopg2.connect(dbname='TS', user='ts',
                        password='6101', host='localhost') #Здесь данные для БД
cursor = conn.cursor()
i = 0
print(Fore.GREEN + 'Создание переменных (config.py): Успех')

while i != 32:
    os.environ['random_data'] += random.choice(string.ascii_letters)
    i+=1

os.environ['command_to_update'] = '/service.' + os.environ.get('random_data')
print(Fore.GREEN + 'SUCCESS CREATED COMMAND (config.py): /' + os.environ.get('command_to_update'))

def is_number(str):
    try:
        balance = int(str)
        return balance
    except ValueError:
        return True
print(Fore.GREEN + 'Создание is_number() (config.py): Успех')
