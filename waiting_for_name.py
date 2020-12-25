#Импорт всех нужных файлов
import telebot
import sys
from config import superadmin, FORMATTER, LOG_FILE, FORMATTER_FILE, get_console_handler, get_file_handler, get_logger
from Keyboards import menu, yesNo, yesNo_for_order, confirm, SCP_5000_keyboard
import PostgreSQL
from time import sleep
from os import environ
from colorama import init, Fore
init(autoreset=True)

print(Fore.GREEN + 'Импорт модулей (waiting_for_name.py): Успех')
log = get_logger('Main messages')

sys.setrecursionlimit(1000000)

# |-------continue_text-------|
# | Функция для регистрации
# | Вызывается для получения имени
# |-------continue_text-------|
def continue_text(message, bot):
    environ['name'] = message.text
    environ['username'] = str(message.from_user.username)

    if PostgreSQL.block(int(environ.get('addr')), True) is True:
        bot.send_message(int(environ.get('addr')), 'Вы *заблокированы*!', parse_mode='Markdown')
        return

    #print(type(addr))
    PostgreSQL.register(int(message.chat.id), environ.get('name'), environ.get('username'))
    bot.send_message(int(message.chat.id), 'Думаю все... \nОжидай когда тебя подтвердят...', reply_markup=menu)
    bot.send_message(superadmin[0], 'Подтвердить пользователя: \nОтправлено: @' + environ.get('username'), reply_markup=confirm)
    environ['status'] = 'None'
print(Fore.GREEN + 'Создание continue_text() (waiting_for_name.py): Успех')

def callback_handler_step2(message, bot):
    balance = message.text
    #print(message.text)

    #print(message.chat.id, '- message.chat.id')
    #print(environ.get('status'), '- status')

    #if message.chat.id != superadmin and status != 'waiting for balance.step1':
    #    print('canceled')
    #    return
    #if balance == True:
    #    bot.send_message(superadmin, '*Нет*, это должно быть целым числом`...`')
    #    status = 'waiting for balance'
    #    print('Zero')
    #    return


    #print(environ.get('addr'))
    #print(balance)
    try:
        int(balance)
    except ValueError:
        log.error(Fore.RED + 'Баланс не целое число, повтор...')
        raise Exception('Это должно быть *целым* числом!')
    log.debug(environ.get('addr'))
    PostgreSQL.confirm(int(environ.get('addr')), message.text)
    #print('confirm OK')
    bot.send_message(int(environ.get('addr')), 'Вы были подтверждены!')
    #print('send_message OK')
    environ['status'] = 'None'
print(Fore.GREEN + 'Создание callback_handler_step2() (waiting_for_name.py): Успех')

def check_balance(message, bot):
    #if message.text.lower() == 'баланс':
    balance = PostgreSQL.balance(message.chat.id)
    PostgreSQL.balance(message.chat.id, True)

    if PostgreSQL.balance(message.chat.id, True) is True:
        bot.send_message(message.chat.id, 'Вы не подтверждены!')
        return

    bot.send_message(message.chat.id, 'Количество _Логиков_ на вашем аккаунте: ' + str(balance[0]), parse_mode='Markdown')
print(Fore.GREEN + 'Создание check_balance() (waiting_for_name.py): Успех')

def create_order_step1(message, bot):
    bot.send_message(message.chat.id, 'Введите username(Без "@") адресата ...')

    environ['status'] = 'waiting for id'
print(Fore.GREEN + 'Создание create_order_step1() (waiting_for_name.py): Успех')

def create_order_step2(message, bot):
    try:
        environ['id'] = str(PostgreSQL.ID_from_username(message.text))
    except Exception as e:
        bot.send_message(message.chat.id, e, parse_mode='Markdown')
        return

    bot.send_message(message.chat.id, 'Введите количество логиков ...')
    environ['status'] = 'waiting for id.step2'
print(Fore.GREEN + 'Создание create_order_step2() (waiting_for_name.py): Успех')

def create_order_step3(message, bot):
    environ['amount'] = message.text

    try:
        int(environ.get('amount'))
    except:
        log.error(Fore.RED + 'Amount состоит не только из цифр')
        raise Exception('Ну, а так-то здесь *должны* быть цифры')

    bot.send_message(message.chat.id, 'Все верно?: \nОтправить на (Подставлено на основе username): ' + environ.get('id') + '\nКоличество: ' + environ.get('amount'), reply_markup=yesNo_for_order)
    environ['status'] = 'None'
    #print(environ.get('status'))
print(Fore.GREEN + 'Создание create_order_step3() (waiting_for_name.py): Успех')

def scp_5000(message, bot):
    send = '''
    Описание: ███-████ - неработающий механический костюм, на внутренних системах которого имеется обозначение "Спецкостюм Абсолютной Изоляции", а производителем указан ████ ███. Предполагается, что ранее ███-████ был наделён рядом аномальных свойств для защиты и поддержки своего носителя, однако полученные в прошлом повреждения оставили во всём костюме только одну рабочую систему - примитивную систему хранения файлов. Все файлы, найденные на ███-████ при обнаружении, содержатся в Архиве 5000-1.

    ███-████ впервые появился в камере содержания ███-579 в Зоне 62C 12 апреля 2020 года. Появление сопровождалось вспышкой света, а внутри костюма был обнаружен труп(Причиной смерти была тупая травма, предположительно, полученная от удара об землю после долгого падения). Генетически труп полностью соответствует сотруднику Фонда Петро Уилсону. В данный момент Петро Уилсон несёт службу в Изолированной Зоне 06(Один из нескольких комплексов, предназначенных для сохранения информации при сдвигах реальности или иных событий временнóй реструктуризации). Применение мнестических препаратов показало, что Уилсон ничего не знает как об ███-████, так и о событиях, описанных в архивах костюма.
    '''
    bot.send_message(message.chat.id, send)
    sleep(82)

    bot.send_message(message.chat.id, 'Архив 5000-1:')
    sleep(0.5)

    bot.send_message(message.chat.id, 'ДНЕВНИК, ЗАПИСЬ 0001-1')
    sleep(0.4)

    send = '''
    Меня зовут Петро Уилсон. Не знаю, что творится. Кажется, кроме меня, никого не осталось.

    День сейчас, гм, ноль второе ноль первое две тысячи двадцатого (простите, сложно надиктовывать (простите, не привык ещё к этой системе, гм)). Сегодня 02.01.2020. Я только что. Я только что сбежал из Изолированной Зоны 06. По-моему… Я не уверен, но по-моему, остальных уже нет в живых. Те мужики, они действовали наверняка. Если б я не забрался в костюм, тогда бы мне и… о Боже.
    '''
    bot.send_message(message.chat.id, send)
    sleep(33)

    bot.send_message(message.chat.id, 'ДНЕВНИК, ЗАПИСЬ 0001-2')
    sleep(0.4)

    send = '''
    Надо мне собраться, а то ничего членораздельного я не запишу. Наверное, полезно будет составить запись всех этих событий, так сказать, для потомков.

    Сейчас я пробираюсь к ближайшему учреждению Фонда - на небольшую явочную точку для агентов, которым надо действовать в этих краях. Вряд ли я там кого-то найду, но наверняка смогу выйти на контакт с начальством и узнать, что же такое происходит.

    Началось всё часов шесть, может семь назад. Этот отряд назвался Мобильной Опергруппой Дзета-19 ("Сам-Один") - может, лазутчики от Повстанцев? Так вот, они вошли в Зону, документы и пароли у них были в порядке, все дела. Собрали всех в столовой, а потом начали пальбу.

    Господи, я… До сих пор чую вкус крови. Никак от этого жуткого металлического привкуса не могу избавиться. Чудо, что в меня не попали и не затоптали, народ так лез друг по другу, лишь бы выбраться. Если б я не залез в Спецкостюм Изоляции, тут бы мне и конец. Без вариантов - я же говорю, эти работали наверняка.

    Я в Иск-Зоне 06 работаю электриком по магистральной сети, так что не совсем в курсе, как эта штука работает, но базовые принципы понимаю. Фильтр восприятия не значит, что меня перестанут видеть - он значит, что они не смогут осознать тот факт, что они меня видят. В конечном итоге без разницы, наверное.

    Но те диверсанты… они даже ничего не брали, даже не пытались. Я, как забрался в эту сбрую, поглядел - слишком страшно было (вот ссыкло, а) взять и сбежать. Они проверили трупы и потом ушли. И каждому - контрольный в голову.

    Они просто пришли всех убивать.
    '''
    bot.send_message(message.chat.id, send)
    sleep(110)

    bot.send_message(message.chat.id, 'ДНЕВНИК, ЗАПИСЬ 0001-3')
    sleep(0.4)

    send = '''
    Несколько часов ноги волок по этой грёбаной пустыне, но наконец-таки добрался до явочной точки. Слышал вдалеке несколько взрывов - может, Фонд отправил МОГ на борьбу с теми диверсантами, пока они не ушли далеко? Надеюсь.

    В жизни так не радовался воде в бутылках. Спецкостюм, как оказалось, поддерживает в теле жизнедеятельность, покуда его носишь, но умом я до сих пор считаю, что должен пить. Так уж человек устроен, наверное.

    Ладно, вот ноги немного отдохнут и попробую запустить тут системы. Надо выйти на контакт с Фондом и выяснить, что вообще творится.
    '''
    bot.send_message(message.chat.id, send)
    sleep(35)

    bot.send_message(message.chat.id, 'ДНЕВНИК, ЗАПИСЬ 0001-3')
    sleep(0.4)
    bot.send_message(message.chat.id, 'Охренеть.')
    sleep(4)

    bot.send_message(message.chat.id, 'ЗАГРУЖЕННЫЙ ФАЙЛ 0001-1')
    sleep(0.4)

    bot.send_message(message.chat.id, 'Контекст: Это разослали во все правительства, во все СМИ и аномальные конторы по всему миру. Пиздец.')
    bot.send_photo(message.chat.id, 'http://scp-ru.wdfiles.com/local--files/scp-5000/skiplogosmall.png')
    send = '''
    Сообщение, приведённое ниже, было составлено при единогласном одобрении Совета О5.

    К сведению тех, кто не осведомлён о нашем существовании: мы представляем организацию, известную как Фонд SCP. В прошлом цель нашей организации заключалась в содержании и исследовании аномальных объектов, сущностей и иных различных явлений. Более ста лет это было ключевой задачей нашей организации.

    По не зависящим от нас обстоятельствам формулировка цели изменилась. Нашей новой целью будет полное уничтожение человеческой расы.

    Других сообщений не будет.
    '''

    bot.send_message(message.chat.id, send)
    sleep(22.15)

    bot.send_message(message.chat.id, 'ПОЛЬЗОВАТЕЛЬСКИЙ ФАЙЛ 0001-1')
    send = '''
    Сразу же после рассылки объявления по всему миру Фонд начал свою атаку на человечество.

    Реакция на аномалии, которые выпустил Фонд, последовала максимально быстро, но оказалась бессильна предотвратить ущерб. Сложно сказать, что конкретно происходит, но оттуда, где я сижу - а я залез в сеть Фонда и слежу за новостями - я кое-что уловил. Запишу всё, что знаю - когда это закончится, если кто останется в живых, то хотя бы им будет известно, что с нами стало.

    SCP-096 - Фотографии лица SCP-096 были распространены в социальных сетях. До того, как фотографии были стёрты, число жертв достигло нескольких сотен. Вполне возможно, что эта тварь до сих пор где-то бегает.

    SCP-169 - В тканях хребта SCP-169 и на его поверхности было подорвано несколько ядерных зарядов, из-за чего объект пошевелился во сне. Возникшие из-за этого землетрясения и цунами стёрли с лица земли множество прибрежных поселений по всему миру.

    SCP-662 - 	В течение 24 часов субъект, внешне похожий на "г-на Работного", появился поблизости от нескольких глав различных государств и убил их с помощью подручных предметов, после чего столь же быстро исчез. Не знаю, почему на второй день они не продолжили эту практику.

    SCP-610 - Внедрённые агенты Фонда распылили образцы SCP-610 во множестве крупных городов, в т.ч. в Нью-Йорке и Дели. Как оказавшиеся поблизости гражданские, так и сами агенты оказались быстро и несовместимо с жизнью заражены SCP-610. Дальнейшее распространение SCP-610 сдерживается совместными усилиями Глобальной Оккультной Коалиции и Церкви Разбитого Бога.

    SCP-682 - Выпущен на волю.

    Не понимаю, почему это происходит.
    '''

    bot.send_message(message.chat.id, send)

    #Привет, нашел пасхалку?
    #Поздравляю, теперь воспроизведи эту пасхалку и получи свои 3 логика
    #Удивительно что ты нашел ЭТО :D
    bot.send_message(message.chat.id, 'Интересно прочитать полностью?', reply_markup=SCP_5000_keyboard)
