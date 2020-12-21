import random
import string
import psycopg2
from colorama import *
from progress.bar import Bar
import os

init(autoreset=True)

os.environ['SECRET_TOKEN'] = 'Сюда токен'
os.environ['name'] = 'None'
os.environ['username'] = 'None'
os.environ['superadmin'] = '799637030'
os.environ['command_to_update'] = '/bdbf0802da04452c385dba8d8cc405976ecb426a55546a11a13226c479e19872f6ce2a3e026b8003fcba508e11c30c0bfa3a9a1fd8e6672fc30de5af10929240'
os.environ['random_data'] = ''
os.environ['id'] = '0'
os.environ['amount'] = '0'
os.environ['status'] = 'None'
os.environ['addr'] = '0'
conn = psycopg2.connect(dbname='', user='',
                        password='', host='localhost') #Здесь данные для БД
cursor = conn.cursor()

bar = Bar('Подготовка...', max = 27)
i = 0

while i != 32:
    os.environ['random_data'] += random.choice(string.ascii_letters)
    i+=1
bar.next() #1

os.environ['command_to_update'] = '/service.' + os.environ.get('random_data')
print(Fore.GREEN + '\nSUCCESS CREATED COMMAND: /' + os.environ.get('command_to_update'))
bar.next() #2

def is_number(str):
    try:
        balance = int(str)
        return balance
    except ValueError:
        return True
bar.next() #3
