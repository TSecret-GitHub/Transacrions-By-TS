# Transacrions-By-TS
![](https://img.shields.io/badge/license-AGPL--3.0-green)
![](https://img.shields.io/badge/version-0.0.2-yellow)
![](https://img.shields.io/badge/platform-telegram-blue)
[![CodeFactor](https://www.codefactor.io/repository/github/tsecret-github/transacrions-by-ts/badge)](https://www.codefactor.io/repository/github/tsecret-github/transacrions-by-ts)

__(Если вам что-то не понятно или у вас что-то не так пишите в Issuies)__
# Настройка
Что-бы бот работал успешно, насколько это возможно, вам нужна база данных `PostgreSQL`.
(Если я не смог вам помочь, то вот: [ссылка](https://bit.ly/38hYq5M))
### Установка на Linux Дистрибутивах на основе Arch
*Шаг первый - установите зависимости*
```bash
$ sudo pacman -S yay
$ yay postgresql pgadmin4
``` 
Здесь мы устанавливаем пакет `yay` - [Yay — Еще один надежный помощник AUR, написанный на GO](https://bit.ly/2WunWPI)
(__Важно заметить - все выполняеться не от root пользователя, а от обычного. `Sudo` - здесь важно__)

*Шаг второй - Настройте службу Postgres*
```bash
sudo -u postgres -i 
initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data/'
exit
sudo systemctl enable --now postgresql
sudo systemctl status postgresql
``` 
По-идее вы должны получить что-то. Это что-то должно иметь хоть какой-то зеленый текст...

*Шаг третий - Установите пароль*
```bash
psql -U postgres
postgres=# \password
```
Сразу вас познакомлю, строка `psql -U postgres` означает - вы вошли в что-то, вроде, консоли сервера. Здесь вы как минимум задаете пароли и создаете свою первую базу данных

*Шаг четвертый - Настройте безопасность подключения*
```bash
$ su
# cd /var/lib/postgres/data
# cp pg_hba.conf pg_hba.conf.backup # in case you mess up
# nano pg_hba.conf
```

> Ваш pg_hba.conf по умолчанию может выглядеть так:
```
 TYPE  DATABASE        USER            ADDRESS                 METHOD
# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            trust
host    replication     all             ::1/128                 trust
```
> «Метод» установлен на доверие, то есть никому не будет запрашивать пароль. Чтобы исправить это, изменить метод от trust к md5 везде.
> И это должно быть все для postgres!
*Шаг шестой - установка PGAdmin 4*

Сначала установим пакет `pgadmin4`:
```bash
sudo pacman -Sy pgadmin4
```
И теперь, если не было никаких ошибок пишем в терминал `pgadmin4`, и дожидаемся загрузки =)
*Шаг седьмой - создание таблиц*
Теперь вам нужна база данных, введите в терминал `pgadmin4` и перейдите по адрессу `http://127.0.0.1:36335/browser/`
Введите данные, а потом:
![](https://i.imgur.com/OG84qxe.png)
Нажмите на "База данных", пот вы увидете это:
![](https://i.imgur.com/jFf6DsV.png)
Заполните и нажмите "Сохранить".
Поздравляю у вас теперб есть база данных! Теперь создайте таблицы, создайте схему с именем `transactions_by_ts`, создайте **в** схеме таблицы `transactions_by_ts.orders` - 
```SQL
CREATE TABLE transactions_by_ts.orders
(
    from_order bigint NOT NULL,
    to_order bigint NOT NULL,
    performed boolean DEFAULT false,
    amount bigint,
    order_id bigint NOT NULL DEFAULT nextval('transactions_by_ts.orders_order_id_seq'::regclass)
)
```
И - 
```SQL
CREATE TABLE transactions_by_ts.users
(
    id bigint NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    balance bigint,
    blocked boolean DEFAULT false
)
```
Возможно у вас это не будет работать, воспльзуйтесь Google что-бы узнать как это сделать:
* https://metanit.com/sql/postgresql/1.2.php
* https://postgrespro.ru/docs/postgresql/9.4/manage-ag-createdb
* https://bit.ly/3rgnTFq

### Установка на других Диструбутивах Linux
К сожалению я использую `Manjaro Linux` и помочь ни чем не могу.
Вот все что я могу дать: [ссылка](https://bit.ly/3mDGdoe)

### Продолжим настройку, теперь ввод данных
Зайдите в файл `config.py`, строка 9 или где возле нее будет строка `os.environ['SECRET_TOKEN'] = 'Сюда токен'`. Получите токет у `@BotFather` и вставте на место текста.
> Как создать бота через Botfather?
> Для создания бота введите в чат с BotFather команду /newbot. Бот попросит вас ввести название для нового бота. Можете указать в любом удобном формате, поддерживается кириллица и латиница, например: «тестовый bot». — Имя будет отображаться в заголовке и в информации о боте.
[Сайт](https://botcreators.ru/blog/kak-sozdat-svoego-bota-v-botfather/#:~:text=%D0%94%D0%BB%D1%8F%20%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%B1%D0%BE%D1%82%D0%B0%20%D0%B2%D0%B2%D0%B5%D0%B4%D0%B8%D1%82%D0%B5%20%D0%B2,%D0%B8%20%D0%B2%20%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BE%20%D0%B1%D0%BE%D1%82%D0%B5.)

Потом строка 19-21: вводите данные сервера(сервер `localhost`)

### Зависимости
```bash
pip install telebot
pip install colorama
pip install time
pip install os
pip install sys
pip install psycopg2
pip install string
pip install random
```

Теперь все **готово**!
А вот теперь мы можем запустить бота:
Зайдите в папку проека и напишите команду: `python 'TransactionBot By TS.py'`
***=)***
