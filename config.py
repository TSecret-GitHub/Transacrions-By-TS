import random
import string
import psycopg2
from colorama import init, Fore
import os
init(autoreset=True)
print(Fore.GREEN + 'Импорт модулей (config.py): Успех')

dbname = os.environ.get('dbname')
user = os.environ.get('user')
password = os.environ.get('password')
os.environ['name'] = 'None'
os.environ['username'] = 'None'
os.environ['superadmin'] = '799637030'
os.environ['command_to_update'] = '/bdbf0802da04452c385dba8d8cc405976ecb426a55546a11a13226c479e19872f6ce2a3e026b8003fcba508e11c30c0bfa3a9a1fd8e6672fc30de5af10929240'
os.environ['random_data'] = ''
os.environ['id'] = '0'
os.environ['amount'] = '0'
os.environ['status'] = 'None'
os.environ['addr'] = '0'
os.environ['SMH'] = 'False' #Separate Message Handler, for admins
conn = psycopg2.connect(dbname=dbname, user=user,
                        password=password, host='localhost') #Здесь данные для БД
cursor = conn.cursor()
i = 0
print(Fore.GREEN + 'Создание переменных (config.py): Успех')

while i != 32:
    os.environ['random_data'] += random.choice(string.ascii_letters)
    i+=1

os.environ['command_to_update'] = '/service.' + os.environ.get('random_data')
print(Fore.GREEN + 'SUCCESS CREATED COMMAND (config.py): /' + os.environ.get('command_to_update'))
